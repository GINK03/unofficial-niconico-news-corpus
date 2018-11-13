import glob
import pandas as pd
import json

df = pd.concat([pd.read_csv(fn, compression='gzip', engine='python') for fn in glob.glob('*.csv.gz')], axis=0)

print(len(df.columns))

term_index = {}
for title, body in zip(df['titles'], df['bodies']):
  try:
    for term in set(title.split()) | set(body.split()):
      if term_index.get(term) is None:
        term_index[term] = len(term_index)
  except Exception as ex:
    print(ex)

ser = json.dumps(term_index, indent=2, ensure_ascii=False)
open('index_term.json', 'w').write(ser)
