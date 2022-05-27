import unittest
from hamcrest import assert_that, equal_to, is_in, empty

from lexer import lex
from lexer import TokenClass as class_

from fixture import load_fixture

CMAVO = None
LUJVO = None


def parse_all(s):
    seq = []
    lex(s, 0, lambda *ls: seq.append(ls))
    return seq


def next_line(li, sep):
    li = li.lstrip()
    if ':' == sep:
        li = li.replace('#', ':')
    word = li.split(sep, 1)[0]
    if word == "natmyrgu'e":
        word = "natmygu'e"
    if word[0] == '.':
        word = word[1:]
    return word


def load_file(fname):
    sep = ':' if 'lujvo' in fname else ' '
    with open(fname) as h:
        words = (next_line(li, sep) for li in h if 'LogFlash' not in li)
        if sep == ':':
            words = filter(lambda w: ' ' not in w, words)
        return set(words)


def load_official_data_fixture():
    global CMAVO, GISMU, LUJVO, RAFSI
    CMAVO = load_file('../data/cmavo.txt')
    LUJVO = load_file('../data/lujvo.txt')
    CMAVO.remove('slaka')
    CMAVO.remove('denpa')


class CmavoTest(unittest.TestCase):

    def test_parse_v(self):
        t = parse_all('.a')

        assert_that(t, equal_to([(class_.SKIP, '.'), (class_.CMAVO, 'a')]))

    def test_parse_cvvv(self):
        t = parse_all("ku'a'e")

        assert_that(t, equal_to([(class_.CMAVO, "ku'a'e")]))

    def test_parse_y(self):
        assert_that(parse_all('y'), equal_to([(class_.CMAVO, 'y')]))
        assert_that(parse_all("y'y"), equal_to([(class_.CMAVO, "y'y")]))

    def test_parse_cy(self):
        assert_that(parse_all('cy'), equal_to([(class_.CMAVO, 'cy')]))

    def test_parse_bu(self):
        def assert_v(v):
            text = f'{v}bu'
            assert_that(parse_all(text), equal_to([(class_.CMAVO, text)]))
            assert_that(parse_all(text), equal_to([(class_.CMAVO, text)]))
        for v in 'aeiouy':  # note the addition of 'y'
            assert_v(v)

    def test_parse_sequence(self):
        t = parse_all("de'epu'o ")

        assert_that(t, equal_to([
            (class_.CMAVO, "de'e"), (class_.CMAVO, "pu'o"), (class_.SKIP, ' ')
            ]))


class BaseTest(unittest.TestCase):

    def test_unknown(self):
        t = parse_all('qqq')

        assert_that(t, equal_to([(class_.UNKNOWN, 'q')] * 3))

    def test_gismu_ccvcv(self):
        t = parse_all('creka')

        assert_that(t, equal_to([(class_.GISMU, 'creka')]))

    def test_gismu_cvccv(self):
        t = parse_all('lijda')

        assert_that(t, equal_to([(class_.GISMU, 'lijda')]))

    def test_skip(self):
        t = parse_all(' .klama. ')

        assert_that(t, equal_to([
            (class_.SKIP, ' .'),
            (class_.GISMU, 'klama'),
            (class_.SKIP, '. ')
            ]))

    def test_rafsi(self):
        t = parse_all('jbobau')

        assert_that(t, equal_to([
            (class_.RAFSI, 'jbo'),
            (class_.RAFSI, 'bau'),
            ]))

    def test_hyphen(self):
        t = parse_all('jbo,r,bau')

        assert_that(t, equal_to([
            (class_.RAFSI, 'jbo'),
            (class_.HYPHEN, ',r,'),
            (class_.RAFSI, 'bau'),
            ]))

    def test_not_hyphen(self):
        t = parse_all('babnoi')

        assert_that(t, equal_to([
            (class_.RAFSI, 'bab'),
            (class_.RAFSI, 'noi'),
            ]))

        t = parse_all('bajram')

        assert_that(t, equal_to([
            (class_.RAFSI, 'baj'),
            (class_.RAFSI, 'ram'),
            ]))

        t = parse_all("bralo'i")

        assert_that(t, equal_to([
            (class_.RAFSI, 'bra'),
            (class_.RAFSI, "lo'i"),
            ]))

    def test_hyphen_after_fourth_letter(self):
        t = parse_all('kulnr,farsi')

        assert_that(t, equal_to([
            (class_.RAFSI, 'kuln'),
            (class_.HYPHEN, 'r,'),
            (class_.GISMU, 'farsi'),
            ]))

    def test_hyphen_after_fifth_letter(self):
        # likely impossible word, but I thought "kulnr,farsi"
        # was not possible but found in the book
        t = parse_all('kulnur,farsi')

        assert_that(t, equal_to([
            (class_.GISMU, 'kulnu'),
            (class_.HYPHEN, 'r,'),
            (class_.GISMU, 'farsi'),
            ]))

    def test_cultural_rafsi(self):
        t = parse_all("tci'ilykemcantutra")  # example 4.77

        assert_that(t, equal_to([
            (class_.RAFSI, "tci'il"),
            (class_.HYPHEN, 'y'),
            (class_.RAFSI, 'kem'),
            (class_.RAFSI, 'can'),
            (class_.GISMU, 'tutra'),
            ]))

    def test_cmavo_despite_sloppy_word_detection(self):
        # The function `is_word()` will return `True` for `mi klama`,
        # but thanks to the logic in the state machine,
        # after `mi` not parsed as rafsi, it will be re-tried as cmavo.
        t = parse_all('mi klama')

        assert_that(t, equal_to([
            (class_.CMAVO, 'mi'),
            (class_.SKIP, ' '),
            (class_.GISMU, 'klama'),
            ]))

    def test_unknown_cc(self):
        t = parse_all('qq klama')

        assert_that(t, equal_to([
            (class_.UNKNOWN, 'q'),
            (class_.UNKNOWN, 'q'),
            (class_.SKIP, ' '),
            (class_.GISMU, 'klama'),
            ]))

    def test_unknown_symbols(self):
        t = parse_all('#_3')

        assert_that(t, equal_to([
            (class_.UNKNOWN, '#'),
            (class_.UNKNOWN, '_'),
            (class_.UNKNOWN, '3'),
            ]))

    def test_quote(self):
        t = parse_all('zoi gy. lalala .gy.')

        assert_that(t, equal_to([
            (class_.CMAVO, 'zoi'),
            (class_.SKIP, ' '),
            (class_.QUOTE_TOKEN, 'gy.'),
            (class_.QUOTATION, ' lalala '),
            (class_.QUOTE_TOKEN, '.gy.'),
            ]))

    def test_parse_mask_token(self):
        t = parse_all('[MASK]klama')

        assert_that(t, equal_to([
            (class_.MARKUP, '[MASK]'),
            (class_.GISMU, 'klama'),
            ]))

    def test_parse_anything(self):
        with open(__file__) as h:
            big_string = h.read()

        t = parse_all(big_string)

        back_string = ''.join(map(lambda item: item[1], t))
        assert_that(back_string, equal_to(big_string))

    def test_regression(self):
        fixture = [
                ['bakcange', 'bak', 'cange'],
                ['cidj,r,spageti', 'cidj', ',r,', 'spa', 'get', 'i'],
                [".cerman. zei", '.', 'cer', 'man', '. ', 'zei'],
                ["patyta'a", 'pat', 'y', "ta'a"],
                ["ba'ostu", "ba'o", 'stu'],
                ["banta'a", 'ban', "ta'a"],
                ["baple'i", 'bap', "le'i"],
                ["ba'urnoi", "ba'u", 'r', 'noi'],
                ["batkyci'a", 'batk', 'y', "ci'a"],
                ]

        for item in fixture:
            t = parse_all(item[0])
            t = list(map(lambda item: item[1], t))

            assert_that(t, equal_to(item[1:]))


class LogFlashTest(unittest.TestCase):

    def setUpClass():
        if LUJVO is None:
            load_official_data_fixture()

    def test_split_lujvo_only_to_rafsi(self):
        for lujvo in sorted(LUJVO):
            t = parse_all(lujvo)

            classes = set(map(lambda item: item[0].name, t))
            classes = classes.difference({'GISMU', 'RAFSI', 'HYPHEN'})

            assert_that(classes, empty(),
                        f'Unexpected parse of "{lujvo}": {t}')

    def test_accept_cmavo(self):
        def assert_cmavo(item, full_cmavo):
            assert_that(item[0], equal_to(class_.CMAVO),
                        f"for cmavo {full_cmavo}")
            assert_that(item[1], is_in(CMAVO), f"for cmavo {full_cmavo}")

        for cmavo in sorted(CMAVO):
            t = parse_all(cmavo)

            while len(t) > 1:
                mod = t.pop()
                if mod[0] == class_.SKIP:
                    assert_that(mod[1], equal_to('.'), f"for cmavo {cmavo}")
                else:
                    assert_cmavo(mod, cmavo)

            assert_cmavo(t[0], cmavo)


class FixtureTest(unittest.TestCase):
    fixture = None

    def setUpClass():
        FixtureTest.fixture = load_fixture('fixture.txt')

    def test_lexer(self):
        for item in self.fixture:
            text = item.text
            expected = item.lex

            t = parse_all(text)
            tokens = [item[1] for item in t]

            assert_that(tokens, equal_to(expected), f'For input: "{text}"')


if __name__ == '__main__':
    load_official_data_fixture()
    unittest.main()
