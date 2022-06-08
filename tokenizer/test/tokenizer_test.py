import unittest
from hamcrest import assert_that, equal_to

import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from jbotokenizer import text_to_tokens  # noqa: E402
from fixture import load_fixture  # noqa: E402


class TokenizerTest(unittest.TestCase):

    def test_cmavo(self):
        t = text_to_tokens('pareci')

        assert_that(t, equal_to(['pa', 're', 'ci']))

    def test_ignore_skippable(self):
        t = text_to_tokens('.pa re  ci .')

        assert_that(t, equal_to(['pa', 're', 'ci']))

    def test_report_gismu(self):
        t = text_to_tokens('klama')

        assert_that(t, equal_to(['klama']))

    def test_expand_rafsi_plus_gismu(self):
        t = text_to_tokens('tceklama')

        assert_that(t, equal_to(['mutce##', 'klama']))

    def test_add_continuation(self):
        t = text_to_tokens('tcesutkla')

        assert_that(t, equal_to(['mutce##', 'sutra##', 'klama']))

    def test_break_continuation(self):
        t = text_to_tokens('tce kla')

        assert_that(t, equal_to(['mutce', 'klama']))

    def test_retain_continuation_on_hyphen(self):
        t = text_to_tokens('tce,r,kla')

        assert_that(t, equal_to(['mutce##', 'klama']))

    def test_4letter_rafsi(self):
        t = text_to_tokens('mutcyklama')

        assert_that(t, equal_to(['mutce##', 'klama']))

    def test_cultural_rafsi(self):
        t = text_to_tokens("tci'ilykemcantutra")  # example 4.77

        assert_that(t, equal_to(["tci'il##", 'ke##', 'canre##', 'tutra']))

    def test_unknown_rafsi(self):
        t = text_to_tokens('rtekla')

        assert_that(t, equal_to(['rte##', 'klama']))

    def test_unknown_token(self):
        t = text_to_tokens('qq qqq')

        assert_that(t, equal_to(['q##', 'q', 'q##', 'q##', 'q']))

    def test_split_quote_to_characters(self):
        t = text_to_tokens('zoi gy. lalala .gy.')

        assert_that(t, equal_to(['zoi', 'gy.', ' ##', 'l##', 'a##',
                                'l##', 'a##', 'l##', 'a##', ' ', '.gy.']))

    def test_report_special_token(self):
        t = text_to_tokens('do [MASK] mi')

        assert_that(t, equal_to(['do', '[MASK]', 'mi']))

    def test_fixture(self):
        fixture = load_fixture('fixture.txt')
        for item in fixture:
            text = item.text
            expected = item.token

            t = text_to_tokens(text)

            assert_that(t, equal_to(expected), f'For input: "{text}"')


if '__main__' == __name__:
    unittest.main()
