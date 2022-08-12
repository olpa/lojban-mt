#!/usr/bin/env python3

import jbotokenizer
import json
import random
from transformers import AutoTokenizer
import os
import xml.etree.ElementTree as ET

from zmifanva_solr_xml_to_bitext import iterate_bitext
from interpret_apply_split import parse_command_line, split_to_indexes


def get_tokenizers():
    jb_tok = jbotokenizer.text_to_tokens

    os.environ.putenv('TOKENIZERS_PARALLELISM', 'false')
    bert_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

    def en_tok(text):
        return bert_tokenizer(text, add_special_tokens=False).tokens()

    return {'jb_tok': jb_tok, 'en_tok': en_tok}


def load_corpus(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    return list(iterate_bitext(root))


def write_split(fname, corpus, index_range, basename, tokenizers):
    print(f"Write {fname} range {index_range} basename {basename}")
    jb_tok = tokenizers['jb_tok']
    en_tok = tokenizers['en_tok']
    split = corpus[index_range[0]:index_range[1]]
    dname = os.path.dirname(fname)
    os.makedirs(dname, exist_ok=True)
    with open(fname, 'w') as h:
        for entry in split:
            jb_text = entry[1]
            en_text = entry[2]
            out_entry = {
                    'id': entry[0],
                    'jb': jb_text,
                    'jb_tok': ' '.join(jb_tok(jb_text)),
                    'en': en_text,
                    'en_tok': ' '.join(en_tok(en_text)),
                    'source': basename,
                    }
            json.dump(out_entry, h)
            h.write('\n')


def main():
    args = parse_command_line()
    print(args)

    corpus = load_corpus(args.input)
    split_idx = split_to_indexes(args.split_spec, len(corpus))
    tokenizers = get_tokenizers()

    random.seed(args.seed)
    random.shuffle(corpus)

    for (out_fname, index_range) in zip(args.file_spec, split_idx):
        write_split(out_fname, corpus, index_range, args.basename, tokenizers)


if '__main__' == __name__:
    main()
