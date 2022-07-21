import sys
from datasets import load_dataset

ds_name, fname = sys.argv[1:]

ds = load_dataset(ds_name)
ds.save_to_disk(fname)
