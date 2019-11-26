from tqdm import tqdm


IGNORE_LINES = ['#', '//']


class Lexicon:

    def __init__(self, entries=None):
        self.entries = entries or {}

    def get(self, word):
        """
        Return transcriptions for the given word.

        Args:
            word (str): Word to get possible transcriptions.

        Returns:
            list: List of lists with tokens.
        """
        return self.entries[word]

    def add(self, word, tokens):
        """
        Add a transcription for the given word.

        Args:
            word (str): Word to add a transcription to.
            tokens (list): List of tokens.
        """
        if word not in self.entries.keys():
            self.entries[word] = []

        if tokens not in self.entries[word]:
            self.entries[word].append(tokens)

    def save(self, path, word_sep=' ', token_sep=' '):
        """
        Save the lexicon in file at the given path.

        Args:
            path (str): Path to write to.
            word_sep (str): Separator to use between word and transcription.
            token_sep (str): Separator to use between tokens of transcription.
        """

        lines = []
        sorted_entries = sorted(self.entries.items(), key=lambda x: x[0])

        for word, transcriptions in sorted_entries:
            if len(transcriptions) > 1:
                print('Ignore additional transcriptions')
            else:
                lines.append('{}{}{}'.format(
                    word,
                    word_sep,
                    token_sep.join(transcriptions[0])
                ))

        # Force newline at end of file
        lines.append('')

        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def symbols(self):
        """
        Return set of occuring symbols in the lexicon.
        """
        symbols = set()

        for word, transcriptions in self.entries.items():
            for t in transcriptions:
                symbols.update(t)

        return symbols

    @classmethod
    def load(cls, path, word_sep=' ', token_sep=' ', alphabet=None,
             skip_invalid_lines=False):
        """
        Load a lexicon from the given path.

        Args:
            path (str): Path to the lexicon.
            word_sep (str): Separator between the word and the tokens.
            token_sep (str): Separator between the different tokens.
            alphabet (Alphabet): If ``token_sep`` is the empty string,
                                 the phone-table is used to decode the
                                 transcription, if available.
            skip_invalid_lines (bool): If ``True``, ignores
                                       invalid entries.

        Returns:
            Lexicon: A parsed lexicon.

        """

        lex = cls()

        with open(path, 'r') as f:
            for l in tqdm(f.readlines(), desc='Load lexicon'):
                line = l.strip()
                is_comment = False

                for ignore_start in IGNORE_LINES:
                    if line.startswith(ignore_start):
                        is_comment = True

                if not is_comment and line not in ['']:
                    parts = line.split(word_sep, maxsplit=1)

                    if len(parts) < 2:
                        if not skip_invalid_lines:
                            raise ValueError('Invalid line: {}'.format(line))
                        else:
                            print('Invalid line: {}'.format(line))
                    else:
                        word, transcription = parts

                        if token_sep == '':
                            tokens = alphabet.decode(transcription.strip())
                        else:
                            tokens = transcription.strip().split(token_sep)

                        lex.add(word, tokens)

        return lex
