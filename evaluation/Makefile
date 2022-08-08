copy-ds: cache/jbo-corpus.data

cache/jbo-corpus.data:
	python3 copy-dataset.py olpa/jbo-corpus $@

#
# Tokenize
#

tok-en-v100: cache/tokenized-v100-en.data

cache/tokenized-v100-en.data: cache/jbo-corpus.data
	python3 tokenize_ds.py \
	  --dataset $< \
	  --src-field en \
	  --tgt-field en-moses-tok \
	  --tokenizer moses-en \
	  --output $@

tok-jb-v100: cache/tokenized-v100-en-jb.data

cache/tokenized-v100-en-jb.data: cache/tokenized-v100-en.data
	python3 tokenize_ds.py \
	  --dataset $< \
	  --src-field jb \
	  --tgt-field jb-tok \
	  --tokenizer jb \
	  --output $@

#
# Translate
#

trans-v100-en-jb: cache/translated-v100-en-jb.data

cache/translated-v100-en-jb.data: cache/tokenized-v100-en-jb.data
	python3 translate-with-moses.py \
	  --dataset $< \
	  --endpoint http://localhost:8123 \
	  --src-field en-moses-tok \
	  --tgt-field jb-moses \
	  --output $@
	docker stop en-jb-100

run-en-jb-100:
	docker run -p 8123:8080 --name en-jb-100 --rm olpa/moses-zf-en-jb:1.0.0

trans-v100-jb-en: cache/translated-v100.data

cache/translated-v100.data: cache/translated-v100-en-jb.data
	python3 translate-with-moses.py \
	  --dataset $< \
	  --endpoint http://localhost:8124 \
	  --src-field jb-tok \
	  --tgt-field en-moses \
	  --output $@
	docker stop jb-en-100

run-jb-en-100:
	docker run -p 8124:8080 --name jb-en-100 --rm olpa/moses-zf-jb-en:1.0.0

trans-v110-en-jb: cache/translated-v110-en-jb.data

cache/translated-v110-en-jb.data: cache/tokenized-v100-en-jb.data
	python3 translate-with-moses.py \
	  --dataset $< \
	  --endpoint http://localhost:8125 \
	  --src-field en-moses-tok \
	  --tgt-field jb-moses \
	  --output $@
	docker stop en-jb-110

run-en-jb-110:
	docker run -p 8125:8080 --name en-jb-110 --rm olpa/moses-zf-en-jb:1.1.0 \
	  /opt/moses/bin/moses --server --server-port 8080 -f /zmifanva/moses_model/en-jb/moses.ini

trans-v110-jb-en: cache/translated-v110.data

cache/translated-v110.data: cache/translated-v110-en-jb.data
	python3 translate-with-moses.py \
	  --dataset $< \
	  --endpoint http://localhost:8126 \
	  --src-field jb-tok \
	  --tgt-field en-moses \
	  --output $@
	docker stop jb-en-110

run-jb-en-110:
	docker run -p 8126:8080 --name jb-en-110 --rm olpa/moses-zf-jb-en:1.1.0 \
	  /opt/moses/bin/moses --server --server-port 8080 -f /zmifanva/moses_model/jb-en/moses.ini

#
# Evaluate
#

eval-jb-en-100: cache/eval-jb-en-100

cache/eval-jb-en-100: cache/translated-v100.data
	python3 calc-bleu.py \
	  --dataset $< \
	  --reference-field en-moses-tok \
	  --translation-field en-moses \
	  | tee $@

eval-en-jb-100: cache/eval-en-jb-100

cache/eval-en-jb-100: cache/translated-v100.data
	python3 calc-bleu.py \
	  --dataset $< \
	  --reference-field jb-tok \
	  --translation-field jb-moses \
	  | tee $@

eval-jb-en-110: cache/eval-jb-en-110

cache/eval-jb-en-110: cache/translated-v110.data
	python3 calc-bleu.py \
	  --dataset $< \
	  --reference-field en-moses-tok \
	  --translation-field en-moses \
	  | tee $@

eval-en-jb-110: cache/eval-en-jb-110

cache/eval-en-jb-110: cache/translated-v110.data
	python3 calc-bleu.py \
	  --dataset $< \
	  --reference-field jb-tok \
	  --translation-field jb-moses \
	  | tee $@

#
# Clean
#

clean:
	rm -f cache/*/*/*
	rm -f cache/*/dataset_dict.json
	find cache -depth -type d -exec rmdir {} ";"
