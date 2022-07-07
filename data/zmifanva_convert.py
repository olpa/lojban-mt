#!/usr/bin/env python3

import json
import random
import os
import xml.etree.ElementTree as ET

from zmifanva_solr_xml_to_bitext import iterate_bitext
from interpret_apply_split import parse_command_line, split_to_indexes


def load_corpus(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    return list(iterate_bitext(root))


def write_split(fname, corpus, index_range, basename):
    print(f"Write {fname} range {index_range} basename {basename}")
    split = corpus[index_range[0]:index_range[1]]
    dname = os.path.dirname(fname)
    os.makedirs(dname, exist_ok=True)
    with open(fname, 'w') as h:
        for entry in split:
            out_entry = {
                    'id': entry[0],
                    'jb': entry[1],
                    'en': entry[2],
                    'source': basename,
                    }
            json.dump(out_entry, h)
            h.write('\n')


def main():
    args = parse_command_line()
    print(args)

    corpus = load_corpus(args.input)
    split_idx = split_to_indexes(args.split_spec, len(corpus))

    random.seed(args.seed)
    random.shuffle(corpus)

    for (out_fname, index_range) in zip(args.file_spec, split_idx):
        write_split(out_fname, corpus, index_range, args.basename)


if '__main__' == __name__:
    main()
