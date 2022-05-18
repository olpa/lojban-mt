---
title: 'Run zmifanva locally'
date: '2022-05-10 17:00:00 +0100'
---

# Run zmifanva locally

Zmifanva is a lojban-to-english and english-to-lojban machine translation system, initially developed by Masato Hagiwara: <https://github.com/mhagiwara/zmifanva>, now forked at <https://github.com/olpa/zmifanva/>.

Zmifanva used to be available online, but it disappeared time ago. I don't plan to resurrect its online apearence, but I've containerized the tool so that anyone can deploy zmifanva to internet.

Or you can run zmifanva locally on your computer using [docker compose](https://docs.docker.com/compose/install/).

```
wget https://raw.githubusercontent.com/olpa/zmifanva/docker-compose.yaml
docker-compose up
```

After the images have been downloaded and the containers have been started, find zmifanva on the port 6543: <http://localhost:6543>.
