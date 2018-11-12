import requests
import json
from pathlib import Path
from hashlib import sha256
import os
import sys
import time
from datetime import datetime 
import random
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus

accs = [ line.strip() for line in open('tokens') ]
def graph_access(url, acc, obj, hashed):
	encoded = quote_plus(str(url))
	print(encoded)
	query = f'https://graph.facebook.com/?id={encoded}&fields=og_object{{engagement}},engagement&access_token={acc}'
	r			= requests.get(query)
	fb_obj	 = json.loads(r.text)
	tdatetime = datetime.datetime.now()
	eval_time = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
	
	obj = {} if obj is None else obj
	obj['url']		 = url
	obj[eval_time] = fb_obj
	if fb_obj.get('error'):
		print('error', fb_obj['error']['message'])
		print(fb_obj)
		if 'Cannot specify an empty identifier' == fb_obj['error']['message']:
			path.unlink()
			time.sleep(5.0)
			return
		time.sleep(30.0)
		return
	datum = json.dumps(obj, indent=2, ensure_ascii=False)
	print(datum) 
	open(f'fb_score/{hashed}', 'w').write( datum )
	time.sleep(1.5)

if '--scan' in sys.argv:
	paths = list(Path('../htmls').glob('*'))
	size = len(paths)
	for index, path in enumerate(random.sample(paths, size)):
		soup = BeautifulSoup(path.open().read())
		url = soup.find('meta', {'property':'og:url'})
		if url is None:
			path.unlink()
			continue
		url = url.get('content')
		key = index%len(accs)
		acc = accs[key]
		print(path, url, key)
		hashed = str(path).split('/')[-1]
		if Path(f'fb_score/{hashed}').exists():
			continue
		graph_access(url, acc, None, hashed)
