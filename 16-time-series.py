import dbm

import pickle

import datetime
db = dbm.open('dataset/14-text.dbm', 'r')

key_values = {}
for key in db.keys():
  obj = pickle.loads( db[key] )
  try:
    dtime = datetime.datetime.strptime(obj['time'], "%Y年%m月%d日 %H時%M分") # 2017年12月26日 15時51分
  except ValueError as ex:
    dtime = datetime.datetime.strptime(obj['time'], "%Y/%m/%d %H:%M") # 2017年12月26日 15時51分

  key = dtime.strftime("%Y-%m-%d")
  if key_values.get(key) is None:
    key_values[key] = []
  key_values[key].append( obj )

for key, values in sorted( key_values.items(), key=lambda x:x[0]):
  print(key, len(values))
