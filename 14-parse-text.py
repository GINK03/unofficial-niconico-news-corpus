import bs4

import MeCab

import dbm

import os

import pickle

import glob

import json

import hashlib
#os.system('cp -r ./dbms /tmp/dbms')
m = MeCab.Tagger("-Owakati")

def _map(name):
  print(name)
  url_vals =  {}
  try:
    db = dbm.open(name, 'c')
  except Exception as ex:
    print(ex)
    return url_vals
  for url in db.keys():
    try:
      if os.path.exists('parsed/' + hashlib.sha256(url).hexdigest()):
        print('already passed', url)
        continue
      html = db[url].decode()
      soup = bs4.BeautifulSoup(html)
      if soup.find('div', {'class':'error_code'}) is not None:
        continue
      title = soup.find("h1") 
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
      open('parsed/' + hashlib.sha256(url).hexdigest(),'w').write( json.dumps( {"time":time, "titles":titles, "bodies":bodies } ) )
    except Exception as ex:
      print(ex)
      ...
  return url_vals

db_14 = dbm.open('14-wakati.dbm', 'c')

names = [name for name in glob.glob('dbms/*')]

#_map( names[0] )
import concurrent.futures
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  for url_vals in exe.map(_map, names):
    for url, val in url_vals.items():
      db_14[url] = val
