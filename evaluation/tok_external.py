# Tokenize with moses

import subprocess
import sys

# -q  quiet
# -b  disable Perl buffering
# -l  [en|de|...]
MOSES_EN_COMMAND = [
        *'docker run -i --rm olpa/moses-tune'.split(),
        *'/opt/moses/scripts/tokenizer/tokenizer.perl -q -b -l en'.split()
        ]

# https://olpa.github.io/lojban-mt/ -> tokenizer
JBOPARSE_COMMAND = 'jboparse.py'


class ExternalTokenizer:
    def __init__(self, command):
        self.command = command

    def execute(self, text):
        pipe = subprocess.Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
        back = pipe.communicate(text)
        if back[1]:
            raise SystemError(f'stderr from the tokenizer: {back[1]}')
        return back[0]

    def batch_tokenize(self, sentences):
        text = '\n'.join(sentences).encode('utf-8')
        back = self.execute(text)
        tokenized = str(back, 'utf-8').split('\n')
        if tokenized and tokenized[-1] == '':
            tokenized.pop()
        assert len(sentences) == len(tokenized), \
               f'Number of input sentences: {len(sentences)}, ' \
               f'number of tokenized sentences: {len(tokenized)}'
        return tokenized


def get_moses_en_tokenizer():
    return ExternalTokenizer(MOSES_EN_COMMAND)


def get_jbo_tokenizer():
    return ExternalTokenizer(JBOPARSE_COMMAND)


if '__main__' == __name__:
    tokenizer = get_jbo_tokenizer()
    text = [li.strip() for li in sys.stdin]
    back = tokenizer.batch_tokenize(tokenizer, text)
    print('\n'.join(back))
