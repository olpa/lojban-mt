# Parallel corpus of Lojban sentences

The corpus as a huggingface dataset: <https://huggingface.co/datasets/olpa/jbo-corpus>.

Usage (requirement: [datasets](https://pypi.org/project/datasets/) library):

```
>>> import datasets

>>> ds = datasets.load_dataset(path='olpa/jbo-corpus')
>>> print(ds)
DatasetDict({
    train: Dataset({
        features: ['id', 'jb', 'en', 'source'],
        num_rows: 8844
    })
    test: Dataset({
        features: ['id', 'jb', 'en', 'source'],
        num_rows: 2688
    })
    validation: Dataset({
        features: ['id', 'jb', 'en', 'source'],
        num_rows: 2681
    })
})
>>> ds['train'][200]
{'id': 'crashcourse.jbo_eng_dict:1221',
 'jb': "e'o do dunda lo kabri be lo ladru mi",
 'en': 'Please give me a glass of milk.',
 'source': 'crashcourse.jbo_eng_dict'}
```

How to use datasets:

- [Course -> 3.Fine-tuning a pretrained model -> Processing the data](https://huggingface.co/course/chapter3/2?fw=pt)
- [Course -> 5.The datasets library -> Time to slice and dice](https://huggingface.co/course/chapter5/3?fw=pt)

## Sources

At the moment, the corpus is [taken from zmifanva](https://github.com/olpa/zmifanva/tree/1.0.0/docs). More sources will eventually come. To mention few:

- [tatoeba](https://tatoeba.org/)
- [sutysisku](https://github.com/La-Lojban/sutysisku/tree/master/data)
- [La-Lojban/phrases](https://github.com/La-Lojban/phrases)

### Contributing

Understand the output and read the sources of zmifanva process:

- `make zmifanva_get`
- `make zmifanva_convert`
- note the use of `seed` parameter

Implement the same process for another data source and create a pull request.
