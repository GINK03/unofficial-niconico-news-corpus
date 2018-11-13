import bs4
#import MeCab
import os
import pickle
import gzip
import concurrent.futures
import glob
import gzip
from pathlib import Path
import json

def _map(arg):
  key, names = arg
  for name in names:
    hashed = name.split('/')[-1]
    if Path(f'parsed/{hashed}').exists():
      continue
    print(name)
    soup = bs4.BeautifulSoup( gzip.decompress(open(name, 'rb').read()) )
    if soup.find('div', {'class':'error_code'}) is not None:
      Path(name).unlink()
      continue

    title = soup.find("div", {'class':'article-text-wrap'}) 
    if title is None: 
      Path(name).unlink()
      continue

    time = soup.find("time", {"class":"article-created-at"})
    if time is None: 
      Path(name).unlink()
      continue
    body = soup.find("section", {"class":"article-body news-article-body"} )
    ccount = soup.find('a', {'class':'article-comment-count'})

    time = time.text
    titles = title.text.strip()
    bodies = body.text.strip()
    ccount = ccount.text.strip() 
    if '�' in bodies:
      Path(name).unlink()
      continue
    obj = {"time":time, 'ccount':ccount, "titles":titles, "bodies":bodies }
    json.dump(obj, fp=open(f'parsed/{hashed}', 'w'), ensure_ascii=False, indent=2)
    print(obj)


key_names = {}
for index, name in enumerate(glob.glob('../htmls/*')):
  key = index%12
  if key_names.get(key) is None:
    key_names[key] = []
  key_names[key].append( name )
key_names = [(key,names) for key,names in key_names.items()]
#[_map(arg) for arg in key_names]
with concurrent.futures.ProcessPoolExecutor(max_workers=12) as exe:
  for url_vals in exe.map(_map, key_names):
    ...
