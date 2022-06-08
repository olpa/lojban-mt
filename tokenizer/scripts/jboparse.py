#!/usr/bin/env python3

import argparse
import sys
from jbotokenizer import lex, tokenize


def parse_command_line():
    parser = argparse.ArgumentParser(
            description='Parse lojban text to tokens')
    parser.add_argument('--lex', dest='do_lex',
                        help='return raw lexical tokens',
                        action='store_true')
    parser.add_argument('-n', dest='do_nl',
                        help='do not output the trailing newline',
                        action='store_false')
    parser.add_argument('text', type=str,
                        help='lojban text', nargs='*')
    return parser.parse_args()


if '__main__' == __name__:
    args = parse_command_line()
    if len(args.text):
        src = [' '.join(args.text)]
    else:
        src = sys.stdin
        args.do_nl = True
    for text in src:
        if args.do_lex:
            lex(text, 0, lambda *ls: print(ls, end=' '))
        else:
            tokenize(text, lambda token: print(token, end=' '))
        if args.do_nl:
            print()
