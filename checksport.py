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
pd.set_option('display.max_columns', 110)
pd.set_option('display.max_rows', 100)
pd.set_option('max_colwidth',100)
import matplotlib.pyplot as plt

# Create connnect 建立與mongoDB連線
client = pymongo.MongoClient(host='192.168.158.128', port=27017)
# assign database 選擇資料庫
db = client.tibame
# assign colection 選擇collection
collection = db.hiyd


# Query specific column from all recipe_raw 選擇要讀取的資料欄位
queryArgs = {}
projectField = {'_id' : True, 'url' : True, 'title' : True, 'lesson' : True, 'lesson_time' : True,
                'strengh' : True, 'describe' : True, 'time' : True, 'author' : True }
# 資料庫記得調整
search_response = db.hiyd.find(queryArgs, projection=projectField)
sport_list = []
for item in search_response:
    sport_list.append(item)

data = pd.json_normalize(sport_list,max_level =10)
print(data)
# print(data['lesson'].head(5))
# data.loc['title']

# data = data.set_index(['健身人餐點'])
# print(data.xs('健身人餐點'))