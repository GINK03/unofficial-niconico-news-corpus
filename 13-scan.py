import requests
import dbm
import time
import concurrent.futures
import random
from pathlib import Path
from hashlib import sha256

base_url = 'http://news.nicovideo.jp/watch/nw{}'
headers = {'User-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}

def _map(arr):
  index, iss = arr
  for i in random.sample(iss, len(iss)):
    try:
      url = base_url.format(i)
      hashed = sha256(bytes(url, 'utf8')).hexdigest()
      if Path('htmls/' + hashed).exists():
        continue
      r = requests.get(base_url.format(i), headers = headers)
      r.encoding = r.apparent_encoding 
      if random.random() < 0.01:
        print(r.text)
      Path('htmls/' + hashed).open('w').write( r.text )
    except Exception as ex:
      print(ex)

arrs = {}
for index, i in enumerate(sorted(range(3_500_000, 4_170_719), key=lambda x:x*-1)):
  key = index%32
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append( i )
arrs = [ (index, iss) for index, iss in arrs.items() ] 
print("start to scan")
#_map(arrs[-1])
with concurrent.futures.ProcessPoolExecutor(max_workers=64) as ex:
  ex.map(_map, arrs) 
