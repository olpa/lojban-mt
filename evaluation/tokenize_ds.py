import argparse
import datasets
import tok_external
import tokenize_jbo


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--src-field', required=True)
    parser.add_argument('--tgt-field', required=True)
    parser.add_argument('--tokenizer',
                        choices=['moses-en', 'jb'], required=True)
    parser.add_argument('--output', required=True)
    return parser.parse_args()


def tokenize(ds, tokenizer, src_field, tgt_field):
    new_splits = {}
    for name, split in ds.items():
        sentences = split[src_field]
        tokenized = tokenizer.batch_tokenize(sentences)
        new_splits[name] = split.add_column(tgt_field, tokenized)
    for name, split in new_splits.items():
        ds[name] = split


def main():
    args = parse_command_line()
    if args.tokenizer == 'moses-en':
        tokenizer = tok_external.get_moses_en_tokenizer()
    elif args.tokenizer == 'jb':
        tokenizer = tokenize_jbo.JboTokenizer()
    else:
        raise RuntimeError(f'Unknown tokenizer: {args.tokenizer}')

    ds = datasets.load_from_disk(args.dataset)
    tokenize(ds, tokenizer, args.src_field, args.tgt_field)
    ds.save_to_disk(args.output)


main()
