# Tokenize with moses

import subprocess
import sys

# -q  quiet
# -b  disable Perl buffering
# -l  [en|de|...]
MOSES_EN_COMMAND = [
        *'docker run --rm olpa/moses-tune'.split(),
        *'/opt/moses/scripts/tokenizer/tokenizer.perl -q -b -l en'.split()
        ]

# https://olpa.github.io/lojban-mt/ -> tokenizer
JBOPARSE_COMMAND = 'jboparse.py'


def get_external_tokenizer(command):
    return subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def get_moses_en_tokenizer():
    return get_external_tokenizer(MOSES_EN_COMMAND)

def get_jbo_tokenizer():
    return get_external_tokenizer(JBOPARSE_COMMAND)

def batch_tokenize(tokenizer, sentences):
    text = '\n'.join(sentences).encode('utf-8')
    back = tokenizer.communicate(text)
    if back[1]:
        raise SystemError(f'stderr from the tokenizer: {back[1]}')
    tokenized = str(back[0], 'utf-8').split('\n')
    if tokenized and tokenized[-1] == '':
        tokenized.pop()
    assert len(sentences) == len(tokenized), f'Number of input sentences: {len(sentences)}, number of tokenized sentences: {len(tokenized)}'
    return tokenized


if '__main__' == __name__:
    #tokenizer = get_moses_en_tokenizer()
    tokenizer = get_jbo_tokenizer()
    text = [li.strip() for li in sys.stdin]
    back = batch_tokenize(tokenizer, text)
    print('\n'.join(back))
