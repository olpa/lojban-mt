# Tokenize with moses

import subprocess
import sys

COMMAND = ['docker', 'run',
        # '-it',
        '--rm', 'olpa/moses-tune',
    '/opt/moses/scripts/tokenizer/tokenizer.perl -l en']

class MosesTokenizer():

    def __init__(self):
        self.pipe = None

    def init(self):
        self.pipe = subprocess.Popen(COMMAND, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def tokenize(self, li):
        #back = self.pipe.communicate(input=li.encode())
        self.pipe.stdin.write(li.encode())
        back = self.pipe.stdout.readline()
        print('back:', back)
        return back

    def close(self):
        self.pipe.terminate()
        self.pipe.wait()
        self.pipe = None


if '__main__' == __name__:
    t = MosesTokenizer()
    t.init()
    while li := sys.stdin.readline():
        back = t.tokenize(li)
        print(back)
    t.close()
