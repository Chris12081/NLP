'''
簡要敘述:
輸入喜愛的食材
輸出10種推薦食譜

'''

import pymongo
import numpy as np
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)
from numpy import dot
import pandas as pd
pd.set_option('display.max_columns', 110)
from numpy.linalg import norm
from gensim.models import word2vec
import time
import pprint
start_time = time.time()

# Create connnect 建立與mongoDB連線
client = pymongo.MongoClient(host='localhost', port=27017)

db = client.tibame
collection = db.recipe_vector_w2vm2
# Query specific column from all recipe_raw 選擇要讀取的資料欄位
queryArgs = {}
projectField = {'url' : True, 'title' : True, 'vector' : True}
search_response = db.recipe_vector_w2vm2.find(queryArgs, projection=projectField)

target_list = []
for item in search_response:
    target_list.append(item)
# 利用DataFrame 將 Kmeans分群編號 join 至 總表
data = pd.DataFrame((list(collection.find())))
data2 = pd.read_csv('./kmeans/kmeans_1027_3.csv')
data3 = data.join(data2.set_index('recipe_id'), on='recipe_id')


#載入 欲使用模型
model = word2vec.Word2Vec.load("./word2vec_1026_v1.model")

# user prefered ingredient
my_prefer = ['牛肉','高麗菜','蒜頭','鮮奶','蘋果','蛋']
# my_prefer = ['雞胸肉','花椰菜','黑胡椒','酪梨','香蕉','鮭魚']
# my_prefer = ['沙拉']
# my_prefer = ['牛肉']
print(my_prefer)
# calculate user-prefered ingredients total vector
wordvec = np.zeros([1,150], dtype = float)
# print(wordvec)
# print(model['雞'])
# print(model['雞胸肉'])
for item in my_prefer:
    try:
        # print(model[item])
        wordvec = wordvec + model[item]
        # print(wordvec)
    except:
        pass
# 偏好食材之平均向量
avgvec = wordvec / len(my_prefer)
# print(avgvec)

def cosine_distance_uservec(uservec, target_list, num):
    cosine_dict = {}
    word_list = []
    # 找尋並取得所輸入菜單的總向量
    a = uservec
    # print(a)
    # a = model[word]
    for item in target_list:
        # if item['title'] != word : # 不跟自己做餘弦相似度計算
        # b = model [item]
        b = item['vector'][0]
        # print(b)
        cos_sim = dot(a, b) / (norm(a) * norm(b))
        # print(cos_sim)
        cosine_dict[item['title']] = cos_sim
    # print(sorted(cosine_dict.items()))
    dist_sort = sorted(cosine_dict.items(), key=lambda dist: dist[1], reverse=True)  ## in Descedning order
    # print(dist_sort[:10])
    for item in dist_sort:
        # print('item[0]:',item[0])
        # print('item[1]:',item[1])
        word_list.append((item[0], item[1]))
    return word_list[0:num]

recommend = cosine_distance_uservec(avgvec,target_list,10)
# print(recommend)
recommend_compare = pd.DataFrame(recommend,columns=['title','recommend'])
# print(recommend_compare)
data4 = recommend_compare.join(data3.set_index('title'), on='title')
pprint.pprint(data4.loc[:,['title','recommend','label']])
print("--- spend %s seconds ---" % (time.time() - start_time))
