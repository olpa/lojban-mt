NAMESPACE="olpa"

moses-builder: .moses-builder

.moses-builder: Dockerfile.moses-builder
	docker build -f $< -t moses-builder .
	touch $@

moses-tool: .moses-tool

.moses-tool: Dockerfile.moses-tool
	docker build -f $< -t moses-tool .
	touch $@

moses-tune: .moses-tune

.moses-tune: Dockerfile.moses-tune
	docker build -f $< -t moses-tune .
	touch $@

run-moses:
	docker run -it \
	  -v $(shell pwd)/share:/share \
	  -v $(shell pwd)/test-baseline.sh:/share/test-baseline.sh \
	  moses-tune
