#!/usr/bin/env python3

# Copy-paste from
# https://github.com/olpa/zmifanva/blob/1.1.0/moses_model/scripts/tokenize_jbo.py
# plus `batch_tokenize`

"""
Script to tokenize and normalize Lojban text.
"""
import sys
import re


def normalize(word):
    """Given a Lojban word, normalize it."""
    return word.strip('.?')


def tokenize(text):
    """Given a Lojban text, tokenize it to a list of words."""
    tokens = [normalize(t) for t in re.split(' +', text)]

    # remove the first 'i'
    if len(tokens) > 0 and tokens[0] == 'i':
        tokens = tokens[1:]
    return tokens


class JboTokenizer:
    def batch_tokenize(self, sentences):
        return [' '.join(tokenize(sent)) for sent in sentences]


def main():
    """Main function"""
    for line in sys.stdin:
        tokens = tokenize(line.rstrip())
        print(' '.join(tokens))


if __name__ == '__main__':
    main()
