NAMESPACE="olpa"

all:

run: run-moses

build: moses-tune

moses-builder: .moses-builder

.moses-builder: Dockerfile.moses-builder
	docker build -f $< -t moses-builder .
	touch $@

moses-tool: .moses-tool

.moses-tool: Dockerfile.moses-tool .moses-builder
	docker build -f $< -t moses-tool .
	touch $@

moses-tune: .moses-tune

.moses-tune: Dockerfile.moses-tune moses-tool
	docker build -f $< -t moses-tune -t olpa/moses-tune .
	touch $@

push:
	docker push olpa/moses-tune

# --

run-moses:
	docker run -it \
	  -v $(shell pwd)/share:/share \
	  -v $(shell pwd)/test-baseline.sh:/share/test-baseline.sh \
	  -v $(shell pwd)/config-ems.ini:/share/baseline-ems/config-ems.ini \
	  $(RUN_MOSES_X) \
	  olpa/moses-tune

run-moses-x:
	xhost local:docker
	make run-moses RUN_MOSES_X='-v /tmp/.X11-unix:/tmp/.X11-unix \
	  -e DISPLAY'
