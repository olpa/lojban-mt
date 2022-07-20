import argparse


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--src-field', required=True)
    parser.add_argument('--tgt-field', required=True)
    parser.add_argument('--tokenizer', choices=['moses-en', 'jb'], required=True)
    parser.add_argument('--output', required=True)
    return parser.parse_args()


def main():
    args = parse_command_line()
    print(args)


main()
