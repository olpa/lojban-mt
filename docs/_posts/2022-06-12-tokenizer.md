---
layout: post
title: 'Lojban tokenizer for machine learning, first version'
---

I've just released the first version of a lojban tokenizer. It is intended for use in machine learning applications and therefore is a bit different from a linguistic tokenizer. In particular, it does sub-word tokenization.

Additionally, there is a lexer, which can be used to develop alternative tokenizers.

Home page: https://github.com/olpa/lojban-mt/tree/master/tokenizer/

Fast start:

```
$ VERSION=1.0.0
$ pip3 install https://github.com/olpa/lojban-mt/releases/download/tokenizer-v${VERSION}/jbotokenizer-${VERSION}.tar.gz

$ echo 'coirodo' | jboparse.py
coi ro do

$ jboparse.py coi ro do
coi ro do

$ jboparse.py coi ro do --lex
(<TokenClass.CMAVO: 2>, 'coi') (<TokenClass.SKIP: 1>, ' ')
(<TokenClass.CMAVO: 2>, 'ro') (<TokenClass.SKIP: 1>, ' ')
(<TokenClass.CMAVO: 2>, 'do')

$ jboparse.py lojbangirz
logji## bangu## girzu

$ python3
>>> from jbotokenizer import text_to_tokens
>>> text_to_tokens('ma nuzba')
['ma', 'nuzba']
```
