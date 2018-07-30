
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn import feature_selection
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import lightgbm as lgb
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import FeatureUnion
import json
import glob
import pickle
import numpy as np
import pandas as pd
print('try to load jsons')

data = []
for n in glob.glob('parsed/*')[:200000]:
  try:
    data.append( json.load(open(n)) )
  except Exception as ex:
    print(ex)
    continue

urls = [d['url'] for d in data] 
print('finish to load jsons')
para = {
  "analyzer": 'word',
  "token_pattern": r'\w{1,}',
  "dtype"     : np.float32,
  "sublinear_tf": True,
  "norm"      : 'l2',
}
def get_col(col_name): return lambda x: x[col_name]
vectorizer = FeatureUnion([
        ('bodies',TfidfVectorizer(
            ngram_range=(1, 1),
            max_features=17000,
            **para,
            preprocessor=get_col('bodies'))),
    ])
print('fit to tfidf')
vectorizer.fit(data)
print('finish tfidf')

arr  = vectorizer.transform(data)
voc  = vectorizer.get_feature_names()

pickle.dump( (arr, voc, urls), open('arr_voc_url.pkl', 'wb') )
