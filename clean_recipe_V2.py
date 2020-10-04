# Data Preprocessing 食譜資料前處理

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

# Connecting to mongoDB
# Create connnect 建立與mongoDB連線
client = pymongo.MongoClient(host='192.168.158.128', port=27017)
# assign database 選擇資料庫
db = client.tibame
# assign colection 選擇collection
collection = db.recipe_raw
# Query specific column from all recipe_raw 選擇要讀取的資料欄位
queryArgs = {}
projectField = {'_id' : True, 'url' : True, 'title' : True, 'author' : True, 'ingredient' : True, 'steps' : True, 'category' : True}
search_response = db.recipe_raw.find(queryArgs, projection=projectField)
recipe_list = []
for item in search_response:
    recipe_list.append(item)

# total recipe numbers 確認資料總數
len(recipe_list)

# 設定辭典
# 開啟 stop word list
stop_word = []
with open('./jieba_data/stopword.txt', 'r', encoding='utf-8') as file:
    txt = file.readlines()
# 過濾掉 txt內的\n
    stop_word = [each.strip('\n') for each in txt]
# 開啟 自定義辭典
with open('./jieba_data/mydict.txt', 'r', encoding='utf-8') as file:
    txt = file.readlines()
# 過濾 權重、詞性、空白
    word_bank = [element.replace(' 10 n','').replace(' 20 n','').strip('\n') for element in txt]

# 讀取辭典
jieba.load_userdict('./jieba_data/mydict.txt')
# 將 嫩、豆腐 確實切開
jieba.suggest_freq(('嫩', '豆腐'), True)
for word in word_bank:
# 確保 辭典內容 確實保留
    jieba.suggest_freq(word, True)
# 刪除辭典字
jieba.del_word('雞胸肉')
jieba.del_word('雞肉')
jieba.del_word('蛋黃')
jieba.del_word('全蛋')
jieba.del_word('雞蛋')
jieba.del_word('雞胸肉片')

# Initial googletrans instance
translator = googletrans.Translator()
word_bank_en = {}
for word in word_bank:
    word_bank_en[word] = (translator.translate(word)).text.lower()
# word_bank_en

def clear():
    os.system('clear')

# 製作食物向量
word_list = []
total_match = []

for n, recipe in enumerate(recipe_list):
    # 食物向量
    food_vector = {}
    try:
        ingredient_step = recipe['ingredient'] + ',' + recipe['steps']

        url = recipe['url']
        title = recipe['title']
        author = recipe['author']
        category = recipe['category']

        print('食譜編號: ', n)
        seg = jieba.cut(ingredient_step, cut_all=False)
        #         print('結巴斷詞後: ', seg)
        #         word_list = word_list + ([item for item in list(seg) if len(item) > 0])
        matched = set(seg).intersection(set(word_bank))

        if len(matched) > 5:
            for each_word in word_bank_en:
                if each_word in list(matched):
                    food_vector[word_bank_en[each_word]] = 1
                else:
                    food_vector[word_bank_en[each_word]] = 0

            # forming recipe record
            vector_dict = {}

            vector_dict['url'] = url
            vector_dict['title'] = title
            vector_dict['author'] = author
            vector_dict['vector'] = food_vector
            vector_dict['category'] = category
            #             print(vector_dict)
            #             save back to mongoDB
            db = client.tibame
            collection = db.recipe_vector_6
            insert_item = vector_dict
            insert_result = db.recipe_vector_6.insert_one(insert_item)

            print(insert_result)
            clear()
        else:
            print('The recipe is not good....')
            clear()
            pass

        total_match = total_match + list(matched)
    except:
        pass

# total_match