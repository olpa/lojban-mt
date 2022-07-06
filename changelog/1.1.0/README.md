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


