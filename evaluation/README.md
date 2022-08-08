# Evaluation

Metrics are calculated by [sacreBLEU](https://github.com/mjpost/sacreBLEU).

English to Lojban

| Version | test BLEU | test chrF2 | test TER | train BLEU | train chrF2 | train TER | val BLEU | val chrF2 | val TER |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0.0 | 80.06 | 77.83 | 142.03 | 91.28 | 94.55 | 15.22 | 93.06 | 99.00 | 14.29 |
| 1.1.0 | 64.12 | 73.29 | 170.44 | 91.57 | 96.14 | 15.22 | 49.53 | 76.75 | 128.61 |

TODO: investigate why the scores of 1.1.0 are worse, despite in interactive experiments 1.1.0 is better.

Lojban to English

| Version | test BLEU | test chrF2 | test TER | train BLEU | train chrF2 | train TER | val BLEU | val chrF2 | val TER |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0.0 | 25.20 | 21.53 | 276.62 | 45.56 | 43.02 | 252.73 | 6.74 | 16.73 | 92.69 |
| 1.1.0 | 39.15 | 62.47 | 237.11 | 49.01 | 47.56 | 224.65 | 17.24 | 23.99 | 119.18 |

The split train/validation/test is for future versions. The versions 1.0.0 and 1.1.0 used other own splits.

# Do an evaluation

High-level description:

- Execute "`make copy-ds`" to get the dataset from huggingface and store in the local cache
- tokenize
- translate
- evaluate
- `make clean`

Details are in [Makefile](./Makefile).
