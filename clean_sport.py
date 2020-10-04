# Data Preprocessing 運動課表資料前處理

# import neccessary libraries and package
import matplotlib
import pandas as pd
import numpy as np
import json
import pymongo
import jieba
import string
import re
import os
import time
import random
import googletrans
import nltk
from IPython.display import clear_output
clear_output(wait=True)
from nltk.stem.lancaster import LancasterStemmer
from collections import Counter
pd.set_option('display.max_columns', 110)
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# 指定辭典
# jieba.set_dictionary('jieba_sport/dict.txt.big')
jieba.load_userdict('./jieba_sport/mydict.txt')
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

# total recipe numbers 確認資料總數
# print(len(sport_list))
# print(sport_list)
# 利用pd.DataFrame 查看表格
data = pd.DataFrame(list(collection.find()))
# print(data)
# 將需要清洗之欄位加入List
list_lesson = []
for i in data['lesson']:
    list_lesson.append(i)
# print(list_lesson)

# Data Merge

list_lesson_merge = ''.join(str(list_lesson))
# print(list_lesson_merge)

re_list_lesson_merge = list_lesson_merge.translate(str.maketrans('', '', string.punctuation))
# print(re_list_lesson_merge)
re_list_lesson_merge_2 = re.sub('[*n]','',re_list_lesson_merge)
# print(re_list_lesson_merge_2)

words_list = jieba.lcut(re_list_lesson_merge_2)
# print(words_list)

words_counter = Counter(words_list)
# print(words_counter)



# 保留字
reserve_words_list = []
with open(file='./jieba_sport/mydict.txt',mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        reserve_words_list.append(line)
# print(reserve_words_list)
# 進行保留字萃取
words_list_reserveword = []
for term in words_list:
    if term in reserve_words_list:
        words_list_reserveword.append(term)
print(words_list_reserveword)
w_counter = Counter(words_list_reserveword)
print(w_counter)