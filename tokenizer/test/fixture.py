from collections import namedtuple
import shlex
import sys

#
# Fixture
#

FixtureEntry = namedtuple('FixtureEntry', 'text lex token')


def lines_to_entry(lines):
    if len(lines) > 3:
        print(f'fixture: too many lines: {lines}', file=sys.stderr)
        return None
    if len(lines) < 2:
        print(f'fixture: need at least two lines: {lines}', file=sys.stderr)
        return None
    text = lines[0]
    lex_line = lines[1]
    tok_line = lines[2] if len(lines) == 3 else lex_line
    lex_line = lex_line.replace("'", '€')
    tok_line = tok_line.replace("'", '€')
    try:
        lex = shlex.split(lex_line)
        tok = shlex.split(tok_line)
    except ValueError as e:
        print(f'fixture: error parsing {lines}, {e}', file=sys.stderr)
        return None
    lex = [s.replace('€', "'") for s in lex]
    tok = [s.replace('€', "'") for s in tok]
    return FixtureEntry(text, lex, tok)


def load_fixture(fname='fixture.txt'):
    entries = []
    cur = []

    def commit_entry():
        if not len(cur):
            return
        entry = lines_to_entry(cur)
        if entry:
            entries.append(entry)
        cur.clear()
    with open(fname) as h:
        for li in h:
            pos = li.find('  #')
            if pos != -1:
                li = li[:pos]
            if li[:1] == '#':
                li = ''
            li = li.strip()
            if len(li):
                cur.append(li)
            else:
                commit_entry()
        commit_entry()
    return entries


#
# Official data
#


def next_logflash_line(li, sep):
    li = li.lstrip()
    if ':' == sep:
        li = li.replace('#', ':')
    word = li.split(sep, 1)[0]
    if word == "natmyrgu'e":
        word = "natmygu'e"
    if word[0] == '.':
        word = word[1:]
    return word


def load_logflash_file(fname):
    sep = ':' if 'lujvo' in fname else ' '
    with open(fname) as h:
        words = (next_logflash_line(li, sep) for li in h
                 if 'LogFlash' not in li)
        if sep == ':':
            words = filter(lambda w: ' ' not in w, words)
        return set(words)


def load_official_cmavo(fname='../data/cmavo.txt'):
    cmavo = load_logflash_file(fname)
    cmavo.remove('slaka')
    cmavo.remove('denpa')
    return cmavo


def load_official_lujvo(fname='../data/lujvo.txt'):
    return load_logflash_file(fname)


#
#
#


if __name__ == '__main__':
    entries = load_fixture('fixture.txt')
    print(entries)
