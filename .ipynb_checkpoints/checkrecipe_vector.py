import matplotlib
import pandas as pd
import numpy as np
import pymongo
import jieba
import json
import string
import re
import os
import time
import random
import nltk
from IPython.display import clear_output
clear_output(wait=True)
from nltk.stem.lancaster import LancasterStemmer
from collections import Counter
# pd.set_option('display.max_columns', 110)
pd.set_option('display.max_rows', 100)
# pd.set_option('max_colwidth',100)
import matplotlib.pyplot as plt

# Create connnect 建立與mongoDB連線
client = pymongo.MongoClient(host='192.168.158.128', port=27017)
# assign database 選擇資料庫
db = client.tibame
# assign colection 選擇collection
collection = db.recipe_vector


# Query specific column from all recipe_raw 選擇要讀取的資料欄位
queryArgs = {}
projectField = {'_id' : True, 'url' : True, 'title' : True, 'author' : True, 'vector' : True, 'category' : True}
search_response = db.recipe_vector.find(queryArgs, projection=projectField)
vector_list = []
for item in search_response:
    vector_list.append(item)

data = pd.json_normalize(vector_list)
# print(data)
# print(data['title'].head(100))
# 查詢食譜向量 某欄位為1時 的食材名稱
pd.set_option('display.max_rows', 300)
a = data.loc[data['vector.brown rice']==1,['title','vector.brown rice']]
print(a)

# data = data.set_index(['健身人餐點'])
# print(data.xs('健身人餐點'))