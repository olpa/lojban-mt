#!/bin/bash

set -eu

OUT_DIR='./.cache/zmifanva'

mkdir -p $OUT_DIR
cd $OUT_DIR

if [ -d zmifanva ] ; then
  echo 'zmifanva is already fetched'
  exit
fi

git clone \
  --depth 1  \
  --filter=blob:none  \
  --no-checkout \
  https://github.com/mhagiwara/zmifanva/
cd zmifanva
git checkout master -- docs
