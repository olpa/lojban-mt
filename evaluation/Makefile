copy-ds: cache/jbo-corpus.data

cache/jbo-corpus.data:
	python3 copy-dataset.py olpa/jbo-corpus $@

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
	docker run -p 8123:8080 --name en-jb-100 olpa/moses-zf-en-jb:1.0.0

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
	docker run -p 8124:8080 --name jb-en-100 olpa/moses-zf-jb-en:1.0.0

eval-jb-en-100: cache/eval-jb-en-100

cache/eval-jb-en-100: cache/translated-v100.data
	python3 calc-bleu.py \
	  --dataset $< \
	  --reference-field en-moses-tok \
	  --translation-field en-moses \
	  | tee $@

clean:
	rm -f cache/*/*/*
	rm -f cache/*/dataset_dict.json
	find cache -depth -type d -exec rmdir {} ";"
