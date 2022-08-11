import argparse
import datasets
import json
from sacrebleu.metrics import BLEU, CHRF, TER
import sys


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--reference-field', required=True)
    parser.add_argument('--translation-field', required=True)
    return parser.parse_args()


def split_to_score(reference, system):
    refs = [[ref] for ref in reference]
    bleu = BLEU(tokenize='none', force=True)
    return {
            'bleu': str(bleu.corpus_score(system, refs)),
            'chrf': str(CHRF().corpus_score(system, refs)),
            'ter': str(TER().corpus_score(system, refs)),
            }


def main():
    args = parse_command_line()
    ds = datasets.load_from_disk(args.dataset)
    report = {
            name: split_to_score(
                reference=[s.lower() for s in split[args.reference_field]],
                system=split[args.translation_field])
            for name, split in ds.items()
            }
    json.dump(report, sys.stdout, indent=2)


main()
