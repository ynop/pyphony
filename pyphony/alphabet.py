import os
import json
import unicodedata

from pyphony import resources


class UnknownSymbolException(Exception):

    def __init__(self, symbol, context=None):
        super(UnknownSymbolException, self).__init__(
            self.gen_message(symbol, context)
        )

        self.unknown_symbol = symbol

    def gen_message(self, symbol, context):
        if context is None:
            return 'Could not find symbol "  {}  " ({})'.format(
                symbol,
                symbol.encode('unicode_escape')
            )
        else:
            return ('Could not find symbol matching '
                    'the begin of "  {}  " ({})').format(
                context,
                [r.encode('unicode_escape') for r in context]
            )


class Symbol:
    """
    Represents a single symbol of a specific alphabet.
    """

    def __init__(self, value, ipa_counterpart=None):
        self.value = value
        self.ipa_counterpart = ipa_counterpart


class Alphabet:
    """
    Represents a collection of symbols of a specific alphabet (e.g. IPA).
    """

    def __init__(self, symbols=None, ignore_symbols=None):
        self.symbols = {p.value: p for p in symbols or []}
        self.ignore_symbols = ignore_symbols or []

    def decompose(self, text):
        """
        Try to decompose symbols that are not in the alphabet.
        If there are symbols in the text not in the alphabet,
        that are composed of multiple unicode symbols,
        they are decomposed and added as separate symbols.
        (e.g. '00f5' to ['006f', '0303']
        """
        chars = []

        for x in text:
            if x not in self.symbols.keys() and \
                    x not in self.ignore_symbols:

                decomp = unicodedata.decomposition(x)

                if len(decomp) > 0:
                    parts = decomp.split(' ')

                    for p in parts:
                        if p not in ['<compat>']:
                            char = chr(int(p, 16))
                            chars.append(char)
                else:
                    chars.append(x)

            else:
                chars.append(x)

        return ''.join(chars)

    def decode(self, transcription, strict=True):
        """
        Convert the phonetic transcriptions to a list of symbols.

        Args:
            transcription (str): The string with the transcription to decode.
            strict (bool): If ``True``, symbols that can't be decode raise
                           an error. If ``False``, non-matching symbols are
                           ignored silently.

        Return:
            list: List of symbols (str).
        """

        decoded = []
        rest = self.decompose(transcription)

        while len(rest) > 0:
            best_match = self.best_matching_start_symbol(rest)

            if best_match is None:
                ignore_match = self.best_matching_start_ignore_symbol(rest)

                if ignore_match is not None:
                    rest = rest[len(ignore_match):]
                elif strict:
                    raise UnknownSymbolException(rest[0], rest)
                else:
                    rest = rest[1:]
            else:
                decoded.append(best_match)
                rest = rest[len(best_match):]

        return decoded

    def best_matching_start_symbol(self, transcription):
        """
        Return the symbol that matches the start of the transcription.
        If multiple symbols match, the longer one is returned.
        If multiple symbols match with the same length the first occurrence
        is returned.
        Return ``None`` if no symbol matches at all.
        """

        best_match = None

        for symbol in self.symbols.keys():
            if transcription.startswith(symbol) and \
                    (best_match is None or len(symbol) > len(best_match)):
                best_match = symbol

        return best_match

    def best_matching_start_ignore_symbol(self, transcription):
        """
        Return the ignore-symbol that matches the start of the transcription.
        If multiple ignore-symbols match, the shorter one is returned.
        If multiple ignore-symbols match with the same length the first
        occurence is returned.
        Return ``None`` if no ignore-symbol matches at all.
        """
        best_match = None

        for sym in self.ignore_symbols:
            if transcription.startswith(sym) and \
                    (best_match is None or len(sym) < len(best_match)):
                best_match = sym

        return best_match

    @classmethod
    def load(cls, path):
        """
        Load alphabet from file.
        """
        with open(path, 'r') as f:
            data = json.load(f)

        symbols = []
        ignore_symbols = []

        if 'ignore' in data.keys():
            ignore_symbols.extend(data['ignore'])

        for symbol_value, info in data['symbols'].items():
            ipa = None

            if 'ipa' in info.keys():
                ipa = info['ipa']

            s = Symbol(symbol_value, ipa_counterpart=ipa)
            symbols.append(s)

        return cls(symbols, ignore_symbols=ignore_symbols)

    @classmethod
    def with_name(cls, name):
        """
        Load the alphabet-file with the given name.
        """
        alphabet_file_path = resources.get_resource_path([
            'alphabets',
            '{}.json'.format(name)
        ])

        if not os.path.isfile(alphabet_file_path):
            raise ValueError(
                'There is no alphabet file with name'.format(name)
            )

        return cls.load(alphabet_file_path)

    @classmethod
    def ipa(cls):
        return cls.with_name('ipa')

    @classmethod
    def sampa(cls):
        return cls.with_name('sampa')

    @classmethod
    def xsampa(cls):
        return cls.with_name('xsampa')

    @classmethod
    def marytts_de(cls):
        return cls.with_name('marytts_de')
