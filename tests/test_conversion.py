import pytest

import pyphony


@pytest.fixture
def converter():
    return pyphony.Converter([
        (['a'], ['A']),
        (['a', 'b'], ['Ab']),
        (['c'], ['C']),
        (['b'], ['B', '8']),
    ])


@pytest.fixture
def lexicon():
    lex = pyphony.Lexicon()

    lex.add('aba', ['a', 'b', 'a'])
    lex.add('aba', ['a', 'b', 'b', 'a'])
    lex.add('acba', ['a', 'c', 'b', 'a'])

    return lex


class TestConverter:

    def test_convert(self, converter):
        res = converter.convert(['a', 'c', 'a', 'b', 'b'])
        assert res == ['A', 'C', 'Ab', 'B', '8']

    def test_convert_raises(self, converter):
        with pytest.raises(pyphony.conversion.MissingMapping):
            converter.convert(['a', 'x', 'a', 'b', 'b'])

    def test_convert_return_errors(self, converter):
        res, err = converter.convert(
            ['a', 'c', 'x', 'a', 'b', 'b'],
            strict=False,
            return_errors=True
        )
        assert res == ['A', 'C', 'Ab', 'B', '8']
        assert err == {'x': 1}

    def test_convert_ignores_symbols(self, converter):
        res = converter.convert(
            ['a', 'c', 'x', 'a', 'b', 'b'],
            ignore_symbols=['x']
        )
        assert res == ['A', 'C', 'Ab', 'B', '8']

    def test_convert_lexicon(self, converter, lexicon):
        res = converter.convert_lexicon(lexicon)

        assert len(res.entries) == 2
        assert res.get('aba')[0] == ['Ab', 'A']
        assert res.get('aba')[1] == ['Ab', 'B', '8', 'A']
        assert res.get('acba')[0] == ['A', 'C', 'B', '8', 'A']

    def test_convert_lexicon_ignores_words(self, converter, lexicon):
        lexicon.add('axba', ['a', 'x'])
        res = converter.convert_lexicon(lexicon, ignore_unmappable_words=True)

        assert len(res.entries) == 2
        assert res.get('aba')[0] == ['Ab', 'A']
        assert res.get('aba')[1] == ['Ab', 'B', '8', 'A']
        assert res.get('acba')[0] == ['A', 'C', 'B', '8', 'A']
