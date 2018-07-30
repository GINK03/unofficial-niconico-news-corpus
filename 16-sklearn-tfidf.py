
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
import numpy as np
import pandas as pd
print('try to load jsons')
data = [json.load(open(n)) for n in glob.glob('parsed/*')]
print('finish to load jsons')
para = {
  "analyzer": 'word',
  "token_pattern": r'\w{1,}',
  "sublinear_tf": True,
  "dtype"     : np.float32,
  "norm"      : 'l2',
  "smooth_idf":False
}
def get_col(col_name): return lambda x: x[col_name]
vectorizer = FeatureUnion([
        ('bodies',TfidfVectorizer(
            ngram_range=(1, 1),
            max_features=10000,
            **para,
            preprocessor=get_col('bodies'))),
        ('titles',TfidfVectorizer(
            ngram_range=(1, 1),
            **para,
            max_features=2000,
            preprocessor=get_col('titles')))
    ])
print('fit to tfidf')
vectorizer.fit(data)
print('finish tfidf')

arr  = vectorizer.transform(data).todense()
voc  = vectorizer.get_feature_names()

df   = pd.DataFrame(arr)
df.columns = voc
print(voc)

df.to_csv('df.csv', index=None)
