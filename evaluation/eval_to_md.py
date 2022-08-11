import json
import os
import re
import sys

ORDER_SPLIT = ['test', 'train', 'validation']
ORDER_METRICS = ['bleu', 'chrf', 'ter']


def mk_changelog_report(eval_report, basename):
    for split_name in ORDER_SPLIT:
        print()
        print(split_name)
        print('```')
        split = eval_report[split_name]
        for metric_name in ORDER_METRICS:
            print(split[metric_name])
        print('```')


def mk_readme_report(eval_report, basename):
    vals = ['', basename]
    re_metric_value = re.compile('= ([0-9.]+)')
    for split_name in ORDER_SPLIT:
        split = eval_report[split_name]
        for metric_name in ORDER_METRICS:
            s = split[metric_name]
            m = re_metric_value.search(s)
            assert m
            vals.append(m.group(1))
    print(' | '.join(vals))


def main():
    eval_file = sys.argv[1]
    with open(eval_file) as h:
         eval_report = json.load(h)
    mk_changelog_report(eval_report, os.path.basename(eval_file))
    mk_readme_report(eval_report, os.path.basename(eval_file))

main()
