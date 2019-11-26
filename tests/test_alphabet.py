import pytest

from pyphony import Alphabet, Symbol, UnknownSymbolException


class TestAlphabet:

    def test_decode(self):
        table = Alphabet([
            Symbol('a'),
            Symbol('bc'),
            Symbol('b'),
            Symbol('y'),
        ])

        res = table.decode('abcyba')
        assert res == ['a', 'bc', 'y', 'b', 'a']

    def test_decode_nonspacing_mark(self):
        nm = chr(int('0303', 16))

        table = Alphabet([
            Symbol('a'),
            Symbol('bc'),
            Symbol('b'),
            Symbol('y'),
            Symbol(nm)
        ])

        res = table.decode('abcy' + nm + 'ba')
        exp = ['a', 'bc', 'y', nm, 'b', 'a']
        assert res == exp

    def test_decode_combined_mark(self):
        # There symbols that actually represent two separate ones
        nm = chr(int('00f5', 16))
        s1 = chr(int('006f', 16))
        s2 = chr(int('0303', 16))

        table = Alphabet([
            Symbol('a'),
            Symbol('bc'),
            Symbol('b'),
            Symbol('y'),
            Symbol(s1),
            Symbol(s2),
        ])

        res = table.decode('abcy' + nm + 'ba')
        exp = ['a', 'bc', 'y', s1, s2, 'b', 'a']
        assert res == exp

    def test_decode_raises_if_phone_no_existsing(self):
        table = Alphabet([
            Symbol('a'),
            Symbol('bc'),
            Symbol('b'),
            Symbol('y'),
        ])

        with pytest.raises(UnknownSymbolException):
            table.decode('afbcyba')
