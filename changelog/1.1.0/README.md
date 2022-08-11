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

test
```
BLEU = 68.35 100.0/79.3/57.1/48.1 (BP = 1.000 ratio = 1.034 hyp_len = 30 ref_len = 29)
chrF2 = 78.05
TER = 113.63
```

train
```
BLEU = 89.01 96.9/90.3/86.7/82.8 (BP = 1.000 ratio = 1.000 hyp_len = 32 ref_len = 32)
chrF2 = 94.50
TER = 30.43
```

validation
```
BLEU = 68.34 100.0/81.8/60.0/44.4 (BP = 1.000 ratio = 1.000 hyp_len = 12 ref_len = 12)
chrF2 = 86.94
TER = 14.29
```

### Lojban to English

test
```
BLEU = 45.85 77.1/67.6/42.4/28.1 (BP = 0.918 ratio = 0.921 hyp_len = 35 ref_len = 38)
chrF2 = 63.27
TER = 237.11
```

train
```
BLEU = 49.58 78.6/55.6/38.5/36.0 (BP = 1.000 ratio = 1.000 hyp_len = 28 ref_len = 28)
chrF2 = 48.09
TER = 224.65
```

validation
```
BLEU = 17.24 58.3/27.3/10.0/5.6 (BP = 1.000 ratio = 1.000 hyp_len = 12 ref_len = 12)
chrF2 = 23.99
TER = 119.18
```
