import glob
import pandas as pd
import json
from collections import Counter
import gzip
from concurrent.futures import ProcessPoolExecutor as PPE


def pmap(arg):
  key, fn = arg
  df = pd.read_csv(fn, compression='gzip', engine='python')

  df['ccount'] = df['ccount'].fillna(0.0)
  df['titles'] = df['titles'].fillna("")
  df['bodies'] = df['bodies'].fillna("")
  print(len(df.columns))
  term_index = json.load(fp=open('index_term.json'))
  fp = gzip.open(f'outputs/train_{key:04d}.vw.gz', 'wt')
  for ccount, title, body in zip(df['ccount'], df['titles'], df['bodies']):
    print(ccount, key)
    flag = 1 if ccount > 5 else -1
    obj = dict(Counter(body.split())) 

    vals = [f'{term_index[term]}:{freq:0.4f}' for term, freq in obj.items() if term_index.get(term) is not None]
    vals = ' '.join(vals)
    line = f'{flag} |f {vals}'
    fp.write(line + '\n')

fns = [(index, fn) for index, fn in enumerate(glob.glob('outputs/*.csv.gz')) ]
with PPE(max_workers=12) as exe:
  exe.map(pmap, fns)
