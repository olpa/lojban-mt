lint:
	flake8

mkrepo:
	huggingface-cli repo create jbo-corpus
	git clone https://huggingface.co/olpa/jbo-corpus
	cd jbo-corpus && git config set credential.helper=store

zmifanva_get:
	./zmifanva_fetch.sh

zf_path=.cache/zmifanva/zmifanva/docs
zf_bases_all=$(basename $(notdir $(wildcard $(zf_path)/*.xml)))
zf_dict_base=jbowiki
zf_bases=$(filter-out $(zf_dict_base), $(zf_bases_all))

zmifanva_convert:
	for base in $(zf_bases); do \
	  ./zmifanva_convert.py \
	    --basename $$base \
	    --seed 42 \
	    --input $(zf_path)/BASENAME.xml \
	    ./jbo-corpus/data/train/BASENAME_train.jsonl:60 \
	    ./jbo-corpus/data/validation/BASENAME_validation.jsonl:20 \
	    ./jbo-corpus/data/test/BASENAME_test.jsonl:20 \
	; done
	./zmifanva_convert.py \
	  --basename $(zf_dict_base) \
	  --input $(zf_path)/BASENAME.xml \
	  ./jbo-corpus/data/train/BASENAME_train.jsonl:100
