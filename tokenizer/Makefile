all:

export PYTHONPATH=../src

.PHONY: test lint

test:
	cd test && python3 -m unittest lexer_test

lint:
	flake8
