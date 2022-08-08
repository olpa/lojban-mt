# 1.1.0 of 30 May 2022

## Changelog

- use moses EMS (Experiment Management System) to optimize the translation model
- delete the pre-generated models from `zmifanva` repository
- split zmifanva corpus on train, validation and test
- generate moses model, containerize it and push to docker hub

[Announce on Reddit](https://www.reddit.com/r/lojban/comments/v28xbs/run_zmifanva_locally/)

## Run

```
docker-compose up
xdg-open http://localhost:6543
```

## Source

- [lojban-mt: tag 1.1.0](https://github.com/olpa/lojban-mt/tree/1.1.0)
- [zmifanva: tag 1.1.0](https://github.com/olpa/zmifanva/tree/1.1.0)
- [generating moses model for zmifanva](https://github.com/olpa/zmifanva/tree/1.1.0/moses_model/scripts)

## Evaluation

### English to Lojban

train
```
BLEU = 91.57 96.9/93.5/90.0/86.2 (BP = 1.000 ratio = 1.000 hyp_len = 32 ref_len = 32)
chrF2 = 96.14
TER = 15.22
```

test
```
BLEU = 64.12 93.8/71.0/56.7/44.8 (BP = 1.000 ratio = 1.032 hyp_len = 32 ref_len = 31)
chrF2 = 73.29
TER = 170.44
```

validation
```
BLEU = 49.53 100.0/52.6/38.9/29.4 (BP = 1.000 ratio = 1.000 hyp_len = 20 ref_len = 20)
chrF2 = 76.75
TER = 128.61
```

### Lojban to English

train
```
BLEU = 49.01 75.0/55.6/38.5/36.0 (BP = 1.000 ratio = 1.000 hyp_len = 28 ref_len = 28)
chrF2 = 47.56
TER = 224.65
```

test
```
BLEU = 39.15 77.1/58.8/33.3/21.9 (BP = 0.918 ratio = 0.921 hyp_len = 35 ref_len = 38)
chrF2 = 62.47
TER = 237.11
```

validation
```
BLEU = 17.24 58.3/27.3/10.0/5.6 (BP = 1.000 ratio = 1.000 hyp_len = 12 ref_len = 12)
chrF2 = 23.99
TER = 119.18
```
