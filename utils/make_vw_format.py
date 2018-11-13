import glob
import pandas as pd
import json
from collections import Counter
import gzip
df = pd.concat([pd.read_csv(fn, compression='gzip', engine='python') for fn in glob.glob('*1.csv.gz')], axis=0)

df['ccount'] = df['ccount'].fillna(0.0)
df['titles'] = df['titles'].fillna("")
df['bodies'] = df['bodies'].fillna("")
print(len(df.columns))

term_index = json.load(fp=open('index_term.json'))
fp = gzip.open('train.vw', 'wt')
for ccount, title, body in zip(df['ccount'], df['titles'], df['bodies']):
  print(ccount)
  print(body)
  flag = 1 if ccount > 5 else 0
  obj = dict(Counter(body.split())) 

  vals = [f'{term_index[term]}:{freq:0.4f}' for term, freq in obj.items() if term_index.get(term) is not None]
  vals = ' '.join(vals)
  line = f'{flag} |f {vals}'
  fp.write(line + '\n')
