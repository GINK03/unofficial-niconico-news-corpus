import bs4

#import MeCab

import dbm

import os

import pickle

import glob
#os.system('cp -r ./dbms /tmp/dbms')
#m = MeCab.Tagger("-Owakati")

def _map(name):
  print(name)
  url_vals =  {}
  try:
    db = dbm.open(name, 'c')
  except Exception as ex:
    return url_vals
  for url in db.keys():
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
    titles = title.text.strip()
    bodies = body.text.strip()
    
    url_vals[url] = pickle.dumps( {"time":time, "titles":titles, "bodies":bodies } )
  return url_vals

db_14 = dbm.open('14-text.dbm', 'c')

names = [name for name in glob.glob('dbms/*')]

import concurrent.futures
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  for url_vals in exe.map(_map, names):
    for url, val in url_vals.items():
      db_14[url] = val
