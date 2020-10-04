#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('python -m pip install --upgrade pip')


# In[1]:


get_ipython().system('pip install wordcloud')
get_ipython().system('pip install certifi --ignore-installed')


# In[ ]:


get_ipython().system('pip install jieba')


# In[10]:


get_ipython().system('pip install googletrans')


# In[3]:


get_ipython().system('mkdir jieba_data')


# In[4]:


get_ipython().system('wget https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big -o jieba_data/dict.txt.big')


# In[52]:


jieba.set_dictionary('jieba_data/dict.txt.big')


# In[53]:


import time


# In[12]:


import googletrans


# In[13]:


from pprint import pprint


# In[14]:


pprint(googletrans.LANGCODES) 


# In[17]:


import random


# In[18]:


from wordcloud import WordCloud


# In[19]:


import matplotlib.pyplot as plt


# In[20]:


from PIL import Image


# In[21]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[22]:


import pymongo


# In[23]:


import pandas as pd


# In[24]:


import jieba


# In[25]:


import re


# In[26]:


import numpy as np


# In[27]:


from collections import Counter


# In[28]:


client = pymongo.MongoClient('192.168.158.128', 27017)


# In[29]:


db = client.tibame


# In[30]:


collection = db.recipe_raw


# In[31]:


data = pd.DataFrame(list(collection.find()))
data


# In[160]:


pd_ing = data['ingredient']


# In[44]:


list_ing = []
for i in data['ingredient']:
    list_ing.append(i)
list_ing


# In[32]:


list_steps = []
for i in data['steps']:
    list_steps.append(i)
list_steps


# # Data Merge

# In[50]:


list_ing_merge = ''.join(str(list_ing[:2000]))
print(type(list_ing_merge))
list_ing_merge


# In[38]:


list_steps_merge = ''.join(str(list_steps[:2000]))
print(type(list_steps_merge))
list_steps_merge


# In[ ]:





# # 中轉英

# In[34]:


translator = googletrans.Translator()


# In[39]:


results = translator.translate('我覺得今天天氣很差')
print(results)
print(results.text)


# In[46]:





# In[47]:





# In[63]:


tra_list_ing = []
item = 1
for i in list_ing[:1000]:
    try:
        print(item)
        item += 1
        results = translator.translate(i)
        print(results.text)
        tra_list_ing.append(results.text)
        sleeptime=random.randint(3, 7)
        time.sleep(sleeptime)
        print('睡 %s 秒'%(sleeptime))
    except TypeError:
        pass
with open ('tra_list_ing.txt','w',encoding='utf-8') as t:
    t.write(str(tra_list_ing))
tra_list_ing


# In[121]:


f = open ('mydict.txt','r',encoding='utf-8')
first_line = f.readlines()
print(first_line)


# In[154]:


for i in first_line:
    results = translator.translate(i)
    print(results.text)
#         tra_dict.append(results.text)
    with open ('tra_mydict.txt','a',encoding='utf-8') as t:
        t.write(results.text+'\n')


# # 資料正規化

# In[96]:


rdata = open('tra_list_ing.txt','r',encoding='utf-8')


# In[74]:


# list_ing_fix =  re.sub('[*\dWA-Za-z/''\\\\]','',list_ing_merge)
# list_ing_fix1 =  re.sub('[*s,⋯⋯⋯⋯⋯⋯⋯⋯]','',list_ing_fix)
# list_ing_fix2 =  re.sub('[*｜（）()]','',list_ing_fix1)


# In[97]:


first_line = rdata.readline()
second_line = rdata.readline()
print(first_line)
# print(second_line, first_line, sep = "\n")


# In[ ]:





# In[113]:


regex_rdata =  re.sub('[\d,]','',first_line)
regex_rdata


# In[291]:


list_ing_fix2


# In[262]:


list_ing_fix1


# #  斷詞

# In[116]:


split_rdata = regex_rdata.split()
split_rdata


# In[ ]:


list_ing_fix2


# In[292]:


ing_words_list = jieba.lcut(list_ing_fix2)


# In[301]:


ing_words_list


# # 保留字

# In[156]:


with open(file='tra_mydict.txt',mode='r', encoding="UTF-8") as file:
    reserve_dict = file.readlines()
reserve_dict


# In[157]:


re_reserve_words_list = []
for i in reserve_dict:
    results =  re.sub('[\s]','',i)
    re_reserve_words_list.append(results)
re_reserve_words_list


# # 食譜保留後數據

# In[160]:


ing_words_list_reserveword = []
for term in split_rdata:
    if term in re_reserve_words_list:
        ing_words_list_reserveword.append(term)
ing_words_list_reserveword


# In[169]:


ing_counter = Counter(ing_words_list_reserveword)
print(type(ing_counter))
ing_counter


# In[164]:


ing_counter_sort = Counter(sorted(ing_words_list_reserveword))
ing_counter_sort


# # 停止字

# In[304]:


stop_words_list = []
with open(file='stop_word.txt',mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        stop_words_list.append(line)
stop_words_list


# In[306]:


ing_words_list = jieba.lcut(list_ing_fix2)
ing_words_list_stopword = []
for term in ing_words_list:
    if term not in stop_words_list:
        ing_words_list_stopword.append(term)
ing_words_list_stopword


# In[314]:


ing_counter = Counter(ing_words_list_stopword)


# In[315]:


ing_counter


# In[316]:


ing_counter_1 = Counter(sorted(ing_words_list))


# In[317]:


ing_counter_1


# In[66]:


with open ('ing_counter.csv','w',encoding='utf-8') as f :
    f.write(str(ing_counter))


# In[ ]:





# # 文字雲

# In[168]:


worldcloud = WordCloud(font_path='./fonts/TaipeiSansTCBeta-Regular.ttf').generate_from_frequencies(ing_counter)


# In[319]:


plt.imshow(worldcloud, interpolation='bilinear')


# In[300]:


plt.axis('off')


# In[ ]:





# In[34]:


plt.show()


# In[ ]:


f = open(r'./test0916.txt',encoding='utf-8')


# In[ ]:


print(f.read())


# In[37]:


queryArgs = {}
projectFeild = {'url' : True , 'ingredient': True}
search_response = db.recipe_raw.find(queryArgs,projectFeild)


# In[38]:


recipe_lst = []
for item in search_response:
    try:
        recipe_lst.append(item['ingredient'])
    except Exception as error_name:
        print(error_name)
        pass


# In[57]:


ingredient_str = ''
for item in recipe_lst:
    try:
        ingredient_str = ingredient_str + item
    except Exception as error_name:
        print(error_name)
        pass


# In[58]:


print(type(ingredient_str))


# In[9]:


queryArgs = {}
projectField = {'url' : True, 'title' : True, 'time' : True, 'author' : True, 'ingredient' : True, 'stpes' : True, 'comment' : True}
search_response = db.recipe_raw.find(queryArgs, projection=projectField)

print(type(search_response))

result_recipe = []
for n, item in enumerate(search_response):
    result_recipe.append(item)


# In[10]:


result_recipe

