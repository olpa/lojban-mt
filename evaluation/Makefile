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

trans100en2jb: cache/tokenized-v100-en-jb.data
	python3 translate-with-moses.py \
	  --dataset $< \
	  --endpoint http://localhost:8123 \
	  --src-field en-moses-tok \
	  --tgt-field jb-moses \
	  --output cache/translated-v100-en-jb.data
	# docker stop jb2en100  # FIXME

run-jb2en100:
	docker run -p 8123:8080 --name jb2en100 olpa/moses-zf-jb-en:1.0.0

clean:
	rm -f cache/*/*/*
	rm -f cache/*/dataset_dict.json
	find cache -depth -type d -exec rmdir {} ";"
