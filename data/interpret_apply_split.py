import argparse
import itertools


def parse_command_line():
    """
    Return:
    - input
    - basename
    - seed
    - file_spec: list of files in order
    - split_spec: list corresponding split values
    - paths: zip(file_spec, split_spec)
    """
    parser = argparse.ArgumentParser(
            description='Create train/dev/test corpus for moses')
    parser.add_argument(
            '--input', dest='input', required=True)
    parser.add_argument(
            '--basename', dest='basename', required=True,
            help='1) value for the placeholder BASENAME in file names ' +
                 '2) goes to the field "source" in the dataset')
    parser.add_argument(
            '--seed', dest='seed', type=int, default=42,
            help='random seed for split')
    parser.add_argument('paths', metavar='base:percentage', nargs='+')
    args = parser.parse_args()

    args.input = args.input.replace('BASENAME', args.basename)
    args.paths = reinterpret_split(args.paths, args.basename)
    args.split_spec = list(map(lambda p: p[1], args.paths))
    args.file_spec = list(map(lambda p: p[0], args.paths))
    return args


def reinterpret_split(paths, basename):
    def path_to_path_and_percentage(path):
        assert ':' in path, f"Path should contain ':', but does not: {path}"
        new_path, s_perc = path.split(':')
        new_path = new_path.replace('BASENAME', basename)
        try:
            perc = float(s_perc)
        except ValueError:
            assert False, f"Should have a number after ':': {path}"
        return (new_path, perc)
    split = list(map(path_to_path_and_percentage, paths))
    total = sum(map(lambda ls: ls[1], split))
    assert int(total) == 100, f"Splits should sum to 100%, got: {total}"
    return split


# for the split 80:20 and the length 1000 return:
# [(0, 799), (799, 999)]
def split_to_indexes(splits, length):
    cum = itertools.accumulate(splits)
    borders = list(map(lambda perc: int(perc * length / 100), cum))
    return list(zip(itertools.chain([0], borders), borders))
