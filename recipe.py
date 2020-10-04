#!/usr/bin/env python
# coding: utf-8

import time
import googletrans
from pprint import pprint
# pprint(googletrans.LANGCODES)
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import pymongo
import pandas as pd
import jieba
import re
import numpy as np
from collections import Counter

client = pymongo.MongoClient('192.168.158.128', 27017)
db = client.tibame
collection = db.recipe_raw
data = pd.DataFrame(list(collection.find()))
pd_ing = data['ingredient']
list_ing = []
for i in data['ingredient']:
    list_ing.append(i)

list_steps = []
for i in data['steps']:
    list_steps.append(i)


def word_bank_translate():
    translator = googletrans.Translator()
    word_bank_en = []
    with open('./mydict.txt', 'r', encoding='utf-8') as file:
        txt = file.readlines()
        word_bank_list = [each.strip('\n') for each in txt]
        for each in word_bank_list:
            translated_result = translator.translate(each)
            output_str = translated_result.text.lower() + '\n'
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
            cache_list = loadFile.readlines()
            return cach_list
    except:
        pass


cache_list = loadCache('./vector_cache.txt')
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
        stem_matched_vec = set([stemmer.stem(word.lower()) for word in ingre_step_list]).intersection(
            set(word_bank_dict.keys()))
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
# # Data Merge

list_ing_merge = ''.join(str(list_ing[:2000]))
print(type(list_ing_merge))

list_steps_merge = ''.join(str(list_steps[:2000]))
print(type(list_steps_merge))

# # 中轉英
translator = googletrans.Translator()
results = translator.translate('我覺得今天天氣很差')
print(results)
print(results.text)

tra_list_ing = []
item = 1
for i in list_ing[:1000]:
    try:
        print(item)
        item += 1
        results = translator.translate(i)
        print(results.text)
        tra_list_ing.append(results.text)
        sleeptime = random.randint(3, 7)
        time.sleep(sleeptime)
        print('睡 %s 秒' % (sleeptime))
    except TypeError:
        pass
with open('tra_list_ing.txt', 'w', encoding='utf-8') as t:
    t.write(str(tra_list_ing))

f = open('mydict.txt', 'r', encoding='utf-8')
first_line = f.readlines()
print(first_line)

for i in first_line:
    results = translator.translate(i)
    print(results.text)
    #         tra_dict.append(results.text)
    with open('tra_mydict.txt', 'a', encoding='utf-8') as t:
        t.write(results.text + '\n')

# # 資料正規化


rdata = open('tra_list_ing.txt', 'r', encoding='utf-8')

first_line = rdata.readline()
second_line = rdata.readline()
print(first_line)

regex_rdata = re.sub('[\d,]', '', first_line)

# #  斷詞
split_rdata = regex_rdata.split()
ing_words_list = jieba.lcut(list_ing_fix2)

# # 保留字

with open(file='tra_mydict.txt', mode='r', encoding="UTF-8") as file:
    reserve_dict = file.readlines()

re_reserve_words_list = []
for i in reserve_dict:
    results = re.sub('[\s]', '', i)
    re_reserve_words_list.append(results)

# # 食譜保留後數據
ing_words_list_reserveword = []
for term in split_rdata:
    if term in re_reserve_words_list:
        ing_words_list_reserveword.append(term)

ing_counter = Counter(ing_words_list_reserveword)
print(type(ing_counter))

ing_counter_sort = Counter(sorted(ing_words_list_reserveword))