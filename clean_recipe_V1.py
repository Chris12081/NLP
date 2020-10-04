import matplotlib
import pandas as pd
import numpy as np
import json
import pymongo
import jieba
import string
import re
import time
import random
import googletrans
import nltk
from nltk.stem.lancaster import LancasterStemmer
from collections import Counter
pd.set_option('display.max_columns', 110)
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

try:
    with open('./vector_cache.txt', 'a+', encoding='utf-8') as file:
        file.close()
except:
    pass



# Create connnect 建立與mongoDB連線
client = pymongo.MongoClient(host='192.168.158.128', port=27017)

# assign database 選擇資料庫
db = client.tibame
# assign colection 選擇collection
collection = db.recipe_raw

# Query specific column from all recipe_raw 選擇要讀取的資料欄位
queryArgs = {}
projectField = {'_id' : True, 'url' : True, 'author' : True, 'ingredient' : True, 'steps' : True, 'category' : True}
search_response = db.recipe_raw.find(queryArgs, projection=projectField)

recipe_list = []
for item in search_response:
    recipe_list.append(item)



def word_bank_translate():
    translator = googletrans.Translator()
    word_bank_en = []
    with open('./jieba_data/mydict.txt', 'r', encoding='utf-8') as file:
        txt = file.readlines()
        word_bank_list = [each.strip('\n') for each in txt]
        for each in word_bank_list:
            translated_result = translator.translate(each)
            output_str = translated_result.text.lower()+'\n'
            with open('./jieba_data/word_bank_en.txt', 'a', encoding='utf-8') as f:
                f.write(output_str)

# Reading word_bank_dict

word_bank_dict = {}
with open('./jieba_data/word_bank_en.txt', 'r', encoding='utf-8') as file:
    txt = file.readlines()
    for each in txt:
        word_bank_dict[each.strip('\n')] = 0


# 儲存
def saveCache(string_to_save):
    with open('./vector_cache.txt', 'a+', encoding='utf-8') as cacheFile:
        out_str = string_to_save + '\n'
        cacheFile.write(out_str)
# 讀取
def loadCache(filePath):
    try:
        with open(filePath, 'r', encoding='utf-8') as loadFile:
            cach_list = loadFile.readlines()
            return cach_list
    except:
        pass


cache_list = loadCache('./vector_cache.txt')
print(cache_list)
# Initial googletrans instance
translator = googletrans.Translator()

for n, each_recipe in enumerate(recipe_list):  ## 上次斷線的位置
    print(n)
    if each_recipe['url'] not in cache_list:

        try:
            ingre_step = each_recipe['ingredient'] + ',' + each_recipe['steps']
        except:
            continue
        # print(ingre_step)
        # print('------------------  Translated and segmented -------------------')
        # Translate into EN
        translated_results = translator.translate(ingre_step)
        no_punctuation_result = translated_results.text.translate(str.maketrans('', '', string.punctuation))
        ingre_step_list = no_punctuation_result.split()
        print(ingre_step_list)
        print('================== Find intersection ===========================')
        # find matched items by using set. 用集合的交集方式找出配對的食材跟做法 ##效果不好

        # Try nltk, put all words back into stem state
        # initial a PorterStemmer() instance
        stemmer = nltk.PorterStemmer()

        original_matched_vec = set([word.lower() for word in ingre_step_list]).intersection(set(word_bank_dict.keys()))
        print(original_matched_vec)
        stem_matched_vec = set([stemmer.stem(word.lower()) for word in ingre_step_list]).intersection(set(word_bank_dict.keys()))
        print(stem_matched_vec)
        union_set = original_matched_vec.union(stem_matched_vec)
        print(union_set)

        # Only maintain recipes with more than 3 elements
        if len(union_set) > 3:
            food_vector = {}
            for key in word_bank_dict:
                if key in union_set:
                    food_vector[key] = 1
                else:
                    food_vector[key] = 0
            print(food_vector)

            vector_dict = {}
            url = each_recipe['url']
            author = each_recipe['author']
            category = each_recipe['category']
            vector_dict['url'] = url
            vector_dict['author'] = author
            vector_dict['vector'] = food_vector
            vector_dict['category'] = category

            db = client.tibame
            collection = db.recipe_vector
            insert_item = vector_dict
            insert_result = db.recipe_vector.insert_one(insert_item)

            saveCache(url)
            print(insert_result)

        print("********************** Next one ********************************")
        time.sleep(random.randrange(4, 8))
    else:
        print(each_recipe['url'], 'Has been vectorized')
        pass