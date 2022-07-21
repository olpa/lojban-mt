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
	  --src-field en \
	  --tgt-field en-moses-tok \
	  --tokenizer jb \
	  --output $@

trans100en2jb:
	python3 translate-with-moses.py --dataset olpa/jbo-corpus --endpoint localhost:1234 --src-field en --tgt-field jb-moses --output translated-1.0.0.xx

clean:
	rm -f cache/*/*/*
	rm -f cache/*/dataset_dict.json
	find cache -type d -exec rmdir {} ";"
