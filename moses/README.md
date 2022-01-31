# moses in docker

Under construction. It is possible to run tutorials.

The containers are not optimized.

## Build

```
make moses-builder
make moses-tool
make moses-tune
```

## Run

```
mkdir share
make run-moses
```

## Execute examples

See <http://www.statmt.org/moses/?n=Moses.Tutorial>, <http://www.statmt.org/moses/?n=Moses.SyntaxTutorial>

On the host:

```
cd share
wget http://www.statmt.org/moses/download/sample-models.tgz
tar zxf sample-models.tgz
cd ..
make run-moses
```

In the docker container:

```
cd /share/sample-models
echo 'das ist ein kleines haus' | moses -f phrase-model/moses.ini
echo 'das ist ein haus' | moses -f string-to-tree/moses.ini
```
