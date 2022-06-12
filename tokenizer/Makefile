all:

.PHONY: test lint

test: test-l test-t

test-l:
	cd test && python3 lexer_test.py

test-t:
	cd test && python3 tokenizer_test.py

lint:
	flake8

rafsi: jbotokenizer/rafsi.py

jbotokenizer/rafsi.py: data/mk_rafsi_to_gismu.py data/rafsi.txt data/gismu.txt
	python3 $+ $@

dist:
	python3 -m build

push:
	$(eval VERSION:=$(shell grep version setup.py | cut -d "'" -f 2))
	gh release create tokenizer-v$(VERSION) ./dist/jbotokenizer-$(VERSION).tar.gz
