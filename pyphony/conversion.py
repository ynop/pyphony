import json
import collections

from tqdm import tqdm

import pyphony
from pyphony import resources


class MissingMapping(Exception):

    def __init__(self, symbol):
        super(MissingMapping, self).__init__(
            'No Mapping for symbol: {}'.format(symbol)
        )

        self.symbol = symbol


class Converter:
    """
    Class to convert transcript from one alphabet to another.
    """

    def __init__(self, mapping):
        self.mapping = mapping

    def convert_lexicon(self, in_lex, strict=True,
                        ignore_symbols=None, return_errors=False,
                        ignore_unmappable_words=False):
        """
        Convert the given lexicon.

        Args:
            in_lex (Lexicon): Input lexicon.
            strict (bool): If ``False``, missing mappings are ignored.
            ignore_symbols (list): List of symbols that can be ignored,
                                   if no mapping is available.
            return_errors (bool): If ``True``, returns a tuple
                                  (out_symbols, errors) containing
                                  failed mappings.
            ignore_unmappable_words (bool): If ``True``, no exception is
                                            thrown if word can't get mapped,
                                            but is just ignored.

        Returns:
            Lexicon: Converted lexicon.
        """
        out_lex = pyphony.Lexicon()
        errors = collections.Counter()

        for entry, transcriptions in tqdm(in_lex.entries.items()):
            for t in transcriptions:
                try:
                    conv, t_errors = self.convert(
                        t,
                        strict=strict,
                        ignore_symbols=ignore_symbols,
                        return_errors=True
                    )
                    errors.update(t_errors)
                    out_lex.add(entry, conv)
                except MissingMapping as ex:
                    if not ignore_unmappable_words:
                        raise ex

        if return_errors:
            return out_lex, errors
        else:
            return out_lex

    def convert(self, in_symbols, strict=True,
                ignore_symbols=None, return_errors=False):
        """
        Convert the given input-symbols to symbols of the target alphabet.

        Args:
            in_symbols (list): List of input symbols.
            strict (bool): If ``False``, missing mappings are ignored.
            ignore_symbols (list): List of symbols that can be ignored,
                                   if no mapping is available.
            return_errors (bool): If ``True``, returns a tuple
                                  (out_symbols, errors) containing
                                  failed mappings.

        Returns:
            list: List of output symbols.
        """
        ignore_symbols = ignore_symbols or []
        rest_in_symbols = list(in_symbols)
        out_symbols = []
        errors = collections.Counter()

        while len(rest_in_symbols) > 0:
            next_match = self.best_match(rest_in_symbols)

            if next_match is not None:
                out_symbols.extend(next_match[1])
                rest_in_symbols = rest_in_symbols[len(next_match[0]):]
            else:
                can_be_ignored = rest_in_symbols[0] in ignore_symbols

                if not can_be_ignored:
                    if strict:
                        raise MissingMapping(rest_in_symbols[0])
                    else:
                        errors.update(rest_in_symbols[:1])

                rest_in_symbols = rest_in_symbols[1:]

        if return_errors:
            return out_symbols, errors
        else:
            return out_symbols

    def best_match(self, symbols):
        """
        Return the best matching mapping for the next possible symbol(s).
        Longer input symbols are prioritized.
        """
        best_match = None

        for in_sym, out_sym in self.mapping:
            matches = True

            for i, x in enumerate(in_sym):
                if len(symbols) <= i:
                    matches = False
                elif symbols[i] != x:
                    matches = False

            if matches and \
                    (best_match is None or len(in_sym) > len(best_match[0])):
                best_match = (in_sym, out_sym)

        return best_match

    @classmethod
    def load(cls, path):
        """
        Create converter based on json-file.
        The json-file contains a dictionary with the mapping of symbols
        from source alphabet to target alphabet.
        """

        with open(path, 'r') as f:
            mapping = json.load(f)

        return cls(mapping)

    @classmethod
    def with_names(cls, src_alphabet, target_alphabet):
        path = resources.get_resource_path([
            'conversion',
            '{}_to_{}.json'.format(
                src_alphabet,
                target_alphabet
            )]
        )

        return cls.load(path)

    @classmethod
    def ipa_to_xsampa(cls):
        return cls.with_names('ipa', 'xsampa')

    @classmethod
    def ipa_to_marytts_de(cls):
        return cls.with_names('ipa', 'marytts_de')

    @classmethod
    def marytts_de_to_ipa(cls):
        return cls.with_names('marytts_de', 'ipa')
