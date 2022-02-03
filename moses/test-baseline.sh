#!/bin/sh

set -e
set -x

# See https://www.statmt.org/moses/?n=Moses.Baseline

# mkdir -p /share/baseline-corpus
# cd /share/baseline-corpus
# wget http://www.statmt.org/wmt13/training-parallel-nc-v8.tgz
# tar zxvf training-parallel-nc-v8.tgz
# wget http://www.statmt.org/wmt12/dev.tgz
# tar zxvf dev.tgz

S=/opt/moses/scripts


# The tokenisation can be run as follows

$S/tokenizer/tokenizer.perl -l en \
    < /share/baseline-corpus/training/news-commentary-v8.fr-en.en \
    > /share/baseline-corpus/news-commentary-v8.fr-en.tok.en

$S/tokenizer/tokenizer.perl -l fr \
    < /share/baseline-corpus/training/news-commentary-v8.fr-en.fr \
    > /share/baseline-corpus/news-commentary-v8.fr-en.tok.fr

# The truecaser first requires training, in order to extract some statistics about the text

$S/recaser/train-truecaser.perl \
     --model /share/baseline-corpus/truecase-model.en --corpus     \
     /share/baseline-corpus/news-commentary-v8.fr-en.tok.en
$S/recaser/train-truecaser.perl \
     --model /share/baseline-corpus/truecase-model.fr --corpus     \
     /share/baseline-corpus/news-commentary-v8.fr-en.tok.fr

# Truecasing uses another script from the Moses distribution

$S/recaser/truecase.perl \
   --model /share/baseline-corpus/truecase-model.en         \
   < /share/baseline-corpus/news-commentary-v8.fr-en.tok.en \
   > /share/baseline-corpus/news-commentary-v8.fr-en.true.en
$S/recaser/truecase.perl \
   --model /share/baseline-corpus/truecase-model.fr         \
   < /share/baseline-corpus/news-commentary-v8.fr-en.tok.fr \
   > /share/baseline-corpus/news-commentary-v8.fr-en.true.fr

# Finally we clean, limiting sentence length to 80

$S/training/clean-corpus-n.perl \
    /share/baseline-corpus/news-commentary-v8.fr-en.true fr en \
    /share/baseline-corpus/news-commentary-v8.fr-en.clean 1 80

#
# Language Model Training
#

# build an appropriate 3-gram language model.

mkdir -p /share/baseline-corpus/lm
cd /share/baseline-corpus/lm
lmplz -o 3 \
    < /share/baseline-corpus/news-commentary-v8.fr-en.true.en \
    > news-commentary-v8.fr-en.arpa.en

# Then you should binarise (for faster loading) the *.arpa.en file using KenLM:

build_binary \
   news-commentary-v8.fr-en.arpa.en \
   news-commentary-v8.fr-en.blm.en

#
# Training the Translation System
#

mkdir -p /share/baseline-corpus/working
cd /share/baseline-corpus/working
$S/training/train-model.perl -root-dir train \
  -corpus /share/baseline-corpus/news-commentary-v8.fr-en.clean                             \
  -f fr -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
  -lm 0:3:/share/baseline-corpus/lm/news-commentary-v8.fr-en.blm.en:8 \
  -mgiza \
  -external-bin-dir /opt/tools | tee training.out

#
# Tuning
#

cd /share/baseline-corpus

$S/tokenizer/tokenizer.perl -l en \
   < dev/news-test2008.en > news-test2008.tok.en
$S/tokenizer/tokenizer.perl -l fr \
   < dev/news-test2008.fr > news-test2008.tok.fr
$S/recaser/truecase.perl --model truecase-model.en \
   < news-test2008.tok.en > news-test2008.true.en
$S/recaser/truecase.perl --model truecase-model.fr \
   < news-test2008.tok.fr > news-test2008.true.fr

cd /share/baseline-corpus/working
$S/training/mert-moses.pl \
  /share/baseline-corpus/news-test2008.true.fr \
  /share/baseline-corpus/news-test2008.true.en \
  /opt/moses/bin/moses train/model/moses.ini \
  | tee mert.out

#
# Testing
#

# You can now run Moses with
#   moses -f /share/baseline-corpus/working/mert-work/moses.ini
# Sample phrase:
# faire revenir les militants sur le terrain et convaincre que le vote est utile .


mkdir /share/baseline-corpus/working/binarised-model
cd /share/baseline-corpus/working
processPhraseTableMin \
   -in train/model/phrase-table.gz -nscores 4 \
   -out binarised-model/phrase-table
processLexicalTableMin \
   -in train/model/reordering-table.wbe-msd-bidirectional-fe.gz \
   -out binarised-model/reordering-table

cat /share/baseline-corpus/working/mert-work/moses.ini \
  | sed -r 's@^PhraseDictionaryMemory (.*)path=.*-table.gz(.*)$@PhraseDictionaryCompact \1path=/share/baseline-corpus/working/binarised-model/phrase-table.minphr\2@' \
  | sed -r 's@^(LexicalReordering .*)path=.*gz$@\1path=/share/baseline-corpus/working/binarised-model/reordering-table@' \
  > /share/baseline-corpus/working/binarised-model/moses.ini

# Loading and running a translation is pretty fast (for this I supplied the French sentence "faire revenir les militants sur le terrain et convaincre que le vote est utile .") :
#   moses -f /share/baseline-corpus/working/binarised-model/moses.ini

#
# BLEU
#

cd /share/baseline-corpus
$S/tokenizer/tokenizer.perl -l en \
   < dev/newstest2011.en > newstest2011.tok.en
$S/tokenizer/tokenizer.perl -l fr \
   < dev/newstest2011.fr > newstest2011.tok.fr
$S/recaser/truecase.perl --model truecase-model.en \
   < newstest2011.tok.en > newstest2011.true.en
$S/recaser/truecase.perl --model truecase-model.fr \
   < newstest2011.tok.fr > newstest2011.true.fr

cd /share/baseline-corpus/working

$S/training/filter-model-given-input.pl \
  filtered-newstest2011 mert-work/moses.ini /share/baseline-corpus/newstest2011.true.fr \
  -Binarizer /opt/moses/bin/processPhraseTableMin

moses            \
   -f /share/baseline-corpus/working/filtered-newstest2011/moses.ini   \
   < /share/baseline-corpus/newstest2011.true.fr                \
   > /share/baseline-corpus/working/newstest2011.translated.en         \
   2> /share/baseline-corpus/working/newstest2011.out 

$S/generic/multi-bleu.perl \
   -lc /share/baseline-corpus/newstest2011.true.en              \
   < /share/baseline-corpus/working/newstest2011.translated.en

X
