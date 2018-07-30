import bs4

import MeCab

import dbm

import os

import pickle

import glob

import json

import hashlib

import random
m = MeCab.Tagger("-Owakati")
base_url = 'http://news.nicovideo.jp/watch/nw{}'

def _map(arr):
  index, iss = arr
  iss = random.sample(iss, len(iss))
  for i in iss:
    url = base_url.format(i)
    try:
      if os.path.exists('parsed/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()):
        print('already passed', url)
        continue
      with open('htmls/' +  hashlib.sha256(bytes(url,'utf8')).hexdigest()) as fp:
        soup = bs4.BeautifulSoup(fp.read())
      if soup.find('div', {'class':'error_code'}) is not None:
        continue

      print(soup.find('link', {'rel':'amphtml'}))
      title = soup.title
      #print(title)

      if title is None: 
        print( url)
        continue

      time = soup.find("time", {"class":"article-created-at"})
      if time is None: 
        print( url )
        continue
      body = soup.find("section", {"class":"article-body news-article-body"} )

      time = time.text
      titles = m.parse(title.text).strip()
      bodies = m.parse(body.text).strip()
      
      print(url)
      open('parsed/' + hashlib.sha256(bytes(url,'utf8')).hexdigest(),'w').write( json.dumps( { "url": url, "time":time, "titles":titles, "bodies":bodies } , ensure_ascii=False, indent=2 ) )
      
    except Exception as ex:
      print(ex)


arrs = {}
for index, i in enumerate(sorted(range(0, 3711531), key=lambda x:x*-1)):
  key = index%32
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append( i )
arrs = [ (index, iss) for index, iss in arrs.items() ] 

#_map( arrs[0] )
print("start to scan")
import concurrent.futures
concurrent.futures.ProcessPoolExecutor(max_workers=16).map(_map, arrs)
