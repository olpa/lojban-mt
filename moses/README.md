# moses in docker

Under construction. It is possible to run tutorials.

The containers are not optimized.

# Build

```
make moses-builder
make moses-tool
make moses-ems
make moses-tune
```

# Run

```
mkdir share
make run-moses
```

# Check it works

See <http://www.statmt.org/moses/?n=Moses.Tutorial>

On the host:

```
cd share
wget http://www.statmt.org/moses/download/sample-models.tgz
tar zxf sample-models.tgz
cd ..
make run-moses
```

In the container:

```
cd /share/sample-models
echo 'das ist ein kleines haus' | moses -f phrase-model/moses.ini
echo 'das ist ein haus' | moses -f string-to-tree/moses.ini
```

# Bigger test

See <https://www.statmt.org/moses/?n=Moses.Baseline>

The commands are stored in `test-baseline.sh`.


# Experiment Management System (EMS)

See <https://www.statmt.org/moses/?n=Moses.Baseline>, the corresponding section.


On the host, run the container with X support:

```
# As a side effect, executes `xhost local:docker`
make run-moses-x
```

In the container:

```
cd /share/baseline-ems
/opt/moses/scripts/ems/experiment.perl \
  -config /share/baseline-ems/config-ems.ini -exec \
  | tee log
cat /share/baseline-corpus/working/experiments/evaluation/report.*
```

It is possible to run the EMS without X support. Add the option `-no-graph` to `experiment.perl`.
