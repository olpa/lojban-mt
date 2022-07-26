# 1.0.0 of 28 February 2022

## Changelog

First milestone of `lojban-mt`.

- moses is containerized
- zmifanva is containerized, both the moses models and the frontend
- using the original moses model from zmifanva

[Announce in google groups](https://groups.google.com/g/lojban/c/SVpqnjCyTyw)

## Run

```
docker-compose up
xdg-open http://localhost:6543
```

## Source

- [lojban-mt: tag 1.0.0](https://github.com/olpa/lojban-mt/tree/1.0.0)
- [zmifanva: tag 1.0.0](https://github.com/olpa/zmifanva/tree/1.0.0)
- READMEs: [moses](https://github.com/olpa/lojban-mt/tree/1.0.0/moses), [containerized zmifanva](https://github.com/olpa/lojban-mt/tree/1.0.0/zmifanva)

## Evaluation

### English to Lojban

train
```
BLEU = 91.28 96.8/93.3/89.7/85.7 (BP = 1.000 ratio = 1.000 hyp_len = 31 ref_len = 31)
chrF2 = 94.55
TER = 15.22
```

validation
```
BLEU = 93.06 100.0/91.7/90.9/90.0 (BP = 1.000 ratio = 1.000 hyp_len = 13 ref_len = 13)
chrF2 = 99.00
TER = 14.29
```

test
```
BLEU = 80.06 100.0/84.0/75.0/65.2 (BP = 1.000 ratio = 1.000 hyp_len = 26 ref_len = 26)",
chrF2 = 77.83
TER = 142.03"
```

### Lojban to English

train
```
BLEU = 45.56 75.0/51.9/34.6/32.0 (BP = 1.000 ratio = 1.000 hyp_len = 28 ref_len = 28)
chrF2 = 43.02
TER = 252.73
```

validation
```
BLEU = 6.74 44.4/6.2/3.6/2.1 (BP = 1.000 ratio = 1.000 hyp_len = 9 ref_len = 9)
chrF2 = 16.73
TER = 92.69"
```

test
```
BLEU = 25.20 68.0/37.5/17.4/9.1 (BP = 1.000 ratio = 1.000 hyp_len = 25 ref_len = 25)
chrF2 = 21.53
TER = 276.62
```
