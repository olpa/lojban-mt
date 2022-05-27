#!/usr/bin/env python3

import sys
# from jbotokenizer import lex  # FIXME
from lexer import lex  # FIXME


def parse_all(s):
    seq = []
    lex(s, 0, lambda *ls: seq.append(ls))
    return seq


if '__main__' == __name__:
    text = ' '.join(sys.argv[1:])
    tokens = parse_all(text)
    print(tokens)
