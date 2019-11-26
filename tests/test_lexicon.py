import pytest

from tests import resources

from pyphony import Lexicon


class TestLexicon:

    def test_save(self, tmp_path):
        target = tmp_path / 'lex.txt'

        lex = Lexicon()
        lex.add('bravo', ['b', 'r', 'a', 'v', 'o'])
        lex.add('alpha', ['a', 'l', 'p', 'h', 'a'])
        lex.save(str(target), word_sep=';', token_sep=' ')

        actual_lines = [
            l.strip()
            for l in target.read_text().strip().split('\n')
        ]

        assert actual_lines == [
            'alpha;a l p h a',
            'bravo;b r a v o',
        ]

    def test_load_word_space_separated(self):
        path = resources.get_resource_path([
            'separator',
            'space.txt'
        ])

        lex = Lexicon.load(path, word_sep=' ', token_sep=' ')

        assert lex.get('alpha') == [['a', 'l', 'p', 'h', 'a']]
        assert lex.get('bravo') == [['b', 'r', 'a', 'v', 'o']]
        assert lex.get('charlie') == [['c', 'h', 'a', 'r', 'l', 'i', 'e']]

    def test_load_word_semicolon_separated(self):
        path = resources.get_resource_path([
            'separator',
            'semicolon.txt'
        ])

        lex = Lexicon.load(path, word_sep=';', token_sep=' ')

        assert lex.get('alpha') == [['a', 'l', 'p', 'h', 'a']]
        assert lex.get('bravo') == [['b', 'r', 'a', 'v', 'o']]
        assert lex.get('charlie') == [['c', 'h', 'a', 'r', 'l', 'i', 'e']]

    def test_load_ignores_empty_lines(self, tmp_path):
        content = [
            'alpha a l p h a',
            '',
            'beta b e t a',
            ''
        ]

        lex_file = tmp_path / 'lex.txt'
        lex_file.write_text('\n'.join(content))

        lex = Lexicon.load(str(lex_file), word_sep=' ', token_sep=' ')

        assert lex.get('alpha') == [['a', 'l', 'p', 'h', 'a']]
        assert lex.get('beta') == [['b', 'e', 't', 'a']]

    def test_load_raises_with_empty_transcription(self, tmp_path):
        content = [
            'alpha a l p h a',
            'charlie ',
            'beta b e t a'
        ]

        lex_file = tmp_path / 'lex.txt'
        lex_file.write_text('\n'.join(content))

        with pytest.raises(ValueError):
            Lexicon.load(str(lex_file), word_sep=' ', token_sep=' ')
