# Lojban tokenizer for machine learning tasks

# Usage

- Use as a command-line tool or as a Python module
- Pass a text through the input stream or through the command-line arguments

```
$ echo 'coirodo' | jboparse.py
coi ro do

$ jboparse.py coi ro do
coi ro do

$ jboparse.py coi ro do --lex
(<TokenClass.CMAVO: 2>, 'coi') (<TokenClass.SKIP: 1>, ' ')
(<TokenClass.CMAVO: 2>, 'ro') (<TokenClass.SKIP: 1>, ' ')
(<TokenClass.CMAVO: 2>, 'do')

$ python3
>>> from jbotokenizer import text_to_tokens
>>> text_to_tokens('ma nuzba')
['ma', 'nuzba']
```

# Features

**Parse anything**: you get a result even for invalid lojban text. Highly likely, the parser recovers as soon as a valid lojban starts.

**Reliable**: a test suite has helped to catch and fix corner cases.

**No dependencies**: no external libraries are used. The parser is a combination of character lookup with some mixin of regexps. You can line-by-line port the parser to another language (C, Rust, whatever).

## Tokenizer

The tokenizer is targeted to natural language processing. To minimize the size of vocabulary and avoid out-of-vocabulary tokens, the tokenizer:

- splits lujvo to rafsi expanded to gismu and
- splits names and borrowed words to smaller chunks. Such result makes no sense to a human, but machine learning should cope with it.

```
$ jboparse.py lojbangirz
logji## bangu## girzu

$ jboparse.py la .alis. citka le spageti
la a li s citka le spati## gento i

$ jboparse.py "me la'o ly. spaghetti .ly."
me la'o ly.  ## s## p## a## g## h## e## t## t## i##   .ly.
```

## Lexer

The lexer provides an input to the tokenizer. Using the lexer you can write your own tokenizer in which, for example, you can reconstruct names and borrowed words to their original form.

```
$ jboparse.py --lex lerfyliste
(<TokenClass.RAFSI: 4>, 'lerf') (<TokenClass.HYPHEN: 5>, 'y')
(<TokenClass.GISMU: 3>, 'liste')

$ jboparse.py --lex la .alis. citka le spageti
(<TokenClass.CMAVO: 2>, 'la') (<TokenClass.SKIP: 1>, ' .')
(<TokenClass.CMAVO: 2>, 'a') (<TokenClass.CMAVO: 2>, 'li')
(<TokenClass.UNKNOWN: 0>, 's') (<TokenClass.SKIP: 1>, '. ')
(<TokenClass.GISMU: 3>, 'citka') (<TokenClass.SKIP: 1>, ' ')
(<TokenClass.CMAVO: 2>, 'le') (<TokenClass.SKIP: 1>, ' ')
(<TokenClass.RAFSI: 4>, 'spa') (<TokenClass.RAFSI: 4>, 'get')
(<TokenClass.CMAVO: 2>, 'i')
```

The invariant: for any input text, the joined output is the same as the input.

## Decoder

Not implemented yet. The task is of low priority. Contribute.

# Installation

```
VERSION=1.0.0
pip3 install https://github.com/olpa/lojban-mt/releases/download/tokenizer-v${VERSION}/jbotokenizer-${VERSION}.tar.gz
```

# API

The lexer and the parser use callback-style API. See the script `jboparse.py` for the sample usage and read pydoc comments for details.

```
import jbotokenizer

help(jbotokenizer.tokenize)
help(jbotokenizer.text_to_tokens)
help(jbotokenizer.lex)
help(jbotokenizer.TokenClass)
```

# License

MIT
