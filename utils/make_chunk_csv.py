import json
from pathlib import Path
import MeCab
import pandas as pd
from concurrent.futures import ProcessPoolExecutor as PPE

def pmap(arg):
  m = MeCab.Tagger('-Owakati')
  key, paths = arg
  #if index > 50000: 
  #  break
  objs = []
  for path in paths:
    obj = json.load(path.open())
    bodies = obj['bodies']
    title  = obj['titles']
    times  = obj['time']
    obj['bodies'] = m.parse(bodies).strip()
    obj['titles'] = m.parse(title).strip()
    objs.append(obj)

  df = pd.DataFrame(objs)
  df.to_csv(f'outputs/parsed_{key:04d}.csv.gz', index=None, compression='gzip')

key_paths = {}
for index, path in enumerate(Path('./parsed').glob('*')):
  key = index%16
  if key_paths.get(key) is None:
    key_paths[key] = []
  key_paths[key].append( path )
key_paths = [(key,paths) for key,paths in key_paths.items()]

with PPE(max_workers=16) as exe:
  exe.map(pmap, key_paths)
