---
layout: post
title: 'Run historical versions'
---
# Run historical versions

I'm doing a third iteration on tuning [moses](https://www.statmt.org/moses/) for translating Lojban, and there are plans to test other systems.

To compare the output from different systems I need to easily run them. To do so, for each version (at the moment, only 1.0.0 and 1.1.0), I've:

- pushed tagged containers to docker hub and
- created a version subdirectory under [lojban-mt/changelog/](https://github.com/olpa/lojban-mt/tree/master/changelog/), with `docker-compose.yaml` and `README.md` files.

To run a version, you go to its directory and execute `docker-compose up`.

Meanwhile I've found a nice example that the versions do differ. For the lojban phrase "coi la mlatu" ("hello cat" where "cat" is a name),

- the version 1.0.0 gives "Hi, Tom cat."
- the version 1.1.0 gives "Hello, a cat.". Not perfect, but much better.
