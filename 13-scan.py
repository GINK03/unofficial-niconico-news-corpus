import requests

import dbm

import time

import concurrent.futures

import random
base_url = 'http://news.nicovideo.jp/watch/nw{}'

headers = {'User-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}

def _map(arr):
  index, iss = arr
  db = dbm.open('dbms/htmls_{:09d}.dbm'.format(index), 'c')
  for i in iss:
    url = base_url.format(i)
    if db.get(url) is not None:
      continue
    r = requests.get(base_url.format(i), headers = headers)
    r.encoding = r.apparent_encoding 
    if random.random() < 0.01:
      print(r.text)
    db[url] = r.text
  db.close()
  time.sleep(1)

arrs = {}
for index, i in enumerate(sorted(range(0, 3195155), key=lambda x:x*-1)):
  key = index%32
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append( i )
arrs = [ (index, iss) for index, iss in arrs.items() ] 
print("start to scan")
#_map(arrs[-1])
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as ex:
  ex.map(_map, arrs) 
