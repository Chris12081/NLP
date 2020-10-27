'''
簡要敘述 :
將 recipe_raw 資料中的 ingredient + steps + comment + category 進行斷詞
僅排除特殊字元
即進行W2V 訓練
並將訓練出來的詞以平均向量方式呈現並存入MongoDB
'''

'''
一筆資料展示:
欄位 :{
    "_id": "5f58abb2226b5c697d13c9ad",
    "url": "https://cookpad.com/tw/%E9%A3%9F%E8%AD%9C/13580912-%E5%81%A5%E8%BA%AB%E4%BA%BA-%E9%9B%9E%E8%83%B8%E8%82%89%E4%B8%BC",
    "title": "健身人 雞胸肉丼",
    "time": "2020年09月06日 10:29",
    "author": "Fish",
    "ingredient": "橄欖油,雞胸肉 適量,紅蘿蔔,高麗菜,全蛋,喜歡的深綠色蔬菜,調味料：黑胡椒、黑豆醬油、料酒,",
    "steps": "雞胸肉切丁（好入口的大小）|雞胸肉煎至兩面金黃 盛出備用|橄欖油低溫炒出紅蘿蔔素|加入高麗菜拌炒至喜歡的硬度|加入調味料小火滾一分鐘|加入雞胸肉拌炒|將料理放到煮熟的五穀飯上|鋪上炒蛋 蔬菜|完成！|",
    "comment": "#今天吃這道",
    "category": "健身"}
'''

import pandas as pd
import numpy as np
import pymongo
import jieba
# pd.set_option('display.max_columns', 110)
pd.set_option('display.max_rows', 110)
import warnings
warnings.filterwarnings('ignore')
import re  # For preprocessing
from gensim.models import word2vec,Word2Vec
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)
import time as t



# Create connnect 建立與mongoDB連線
client = pymongo.MongoClient(host='192.168.158.128', port=27017)

# assign database 選擇資料庫
db = client.tibame
# assign colection 選擇collection
collection = db.recipe_raw

# Query specific column from all recipe_raw 選擇要讀取的資料欄位
queryArgs = {}
projectField = {'_id' : True, 'url' : True, 'title' : True,'time' : True, 'author' : True, 'ingredient' : True, 'steps' : True,'comment' : True, 'category' : True}
search_response = db.recipe_raw.find(queryArgs, projection=projectField)
recipe_list = []
for item in search_response:
    recipe_list.append(item)

def jieba_recipe(dicx,data_list,pre_w2v_txt):
    # 自定義辭典斷並將 integration 斷詞後 存入新的collection
    jieba.set_dictionary(dicx)
    start = t.time()
    w2v_list=[]
    title_list=[]
    for n,i in enumerate(data_list):
        try:
            w2v_one = []
            url = i['url']
            title = i['title'].replace(',','-')
            time = i['time']
            author = i['author']
        except:
            pass
        try:
            vector_raw = i['ingredient']+','+i['steps']+','+i['comment']+','+i['category']

            # 進行資料清洗 特殊字元
            vector_clean_1 = re.sub(r'\W', "", vector_raw)
            vector_clean_2 = re.sub(r'[A-Za-z0-9]', "", vector_clean_1)
            vector_clean_3 = re.sub(r'[\U0000FF10-\U0000FF5A]', "", vector_clean_2)  # 過濾全形英文、數字(UTF-32 Big-Endian)
            seg = jieba.lcut(vector_clean_3,cut_all=False) # 精準模式
            # print(seg)
            vec = ' '.join(seg)
            w2v_list.append(vec)
            title_list.append(title)
            # 存成txt
            vec_n = vec + '\n'
            if pre_w2v_txt == 0:
                pass
            else :
                with open(pre_w2v_txt, 'a', encoding='utf-8') as x:
                    x.write(vec_n)
        except :
            continue
    # print(w2v_list)
    end =  t.time()
    print('step1 執行時間:%f 秒'%(end - start))
    print(w2v_list)
    return w2v_list



def w2v_built_save(sourse,savename):
    '''
    min_count: 用於過濾操作，詞頻少於 min_count 次數的單詞會被丟棄掉，預設值為 5
    size: 詞向量的維度。
    workers: 控制訓練的並行數量。
    window: 表示在一個句子中，當前詞於預測詞在一個句子中的最大距離。 window=3
    sg: 用於設定訓練演算法。當 sg=0，使用 CBOW 演算法來進行訓練；當 sg=1，使用 skip-gram 演算法來進行訓練。
    '''
    start2 = t.time()
    sentences = word2vec.LineSentence(sourse)
    # print(sentences)
    model = Word2Vec(sentences, size=150, sg=0, window=3, workers=5)

    # print(len(model.wv.vocab))
    model.save(savename)
    # print(model.corpus_total_words)
    '''
    減醣低碳彩虹生乳酪蛋糕
    低卡鹽水雞胸拌黃瓜
    奶油干貝燒
    鹽麴檸檬烤雞腿
    泰式酸辣瀑布牛肉沙拉
    '''
    # word = '牛'
    # word2 = '雞'

    # print('您選的菜單為: ',word)
    # cosmul = model.wv.most_similar_cosmul(positive=[word,word2],topn=5)
    # print(cosmul)
    # compare = model.wv.similarity(word, word2)
    # print(compare)
    # print('兩菜單比較: ',compare)
    # print('相似度比較: ',model.most_similar(word)[:5])
    # print('菜單向量:',model[word])

    end2 =  t.time()
    print('step2 執行時間:%f 秒'%(end2 - start2))


# 以詞向量存回mongoDB
# forming recipe record
def save_vector(collect,model):
    model = word2vec.Word2Vec.load(model)
    for n,i in enumerate(recipe_list):
        try:
            url = i['url']
            title = i['title'].replace(',','-')
            time = i['time']
            author = i['author']
            vec = list(w2v_list[n].split(' '))
            # print(vec)
            wordvec = np.zeros([1, 150], dtype=float)

            for item in vec:
                try:
                    wordvec = wordvec + model[item]
                except:
                    pass
            avgvec = wordvec / len(vec)
            vector_dict = {}
            vector_dict['recipe_id']=n
            vector_dict['url'] = url
            vector_dict['title'] = title
            vector_dict['time'] = time
            vector_dict['author'] = author
            vector_dict['vector'] = avgvec.tolist()

            # save back to mongoDB
            db = client.tibame
            collection = collect
            insert_item = vector_dict
            insert_result = collect.insert_one(insert_item)
            print(n,title)
            print(insert_result)
        except:
            pass

if __name__ == '__main__':
    jieba_recipe('./jieba_data/dict1026.txt', recipe_list,0)  # 進行斷詞 (左邊填入自定義辭典位置,中間填入欲進行斷字的List,右邊填入斷詞存檔名稱(用於w2v訓練,不儲存請填入0))
    w2v_built_save("./pre_tomodel1026.txt",'word2vec_1026_v1.model') # 進行 w2v 模型建立 並儲存 (左邊為用於w2v訓練之txt檔案,右邊填入選擇的模型名稱)
    w2v_list = jieba_recipe('./jieba_data/dict1026.txt', recipe_list) # 將w2v_list讀出來 以利於 save_vector 使用
    save_vector(db.recipe_vector_w2vm2,"./word2vec_1026_v1.model") # 將 w2v_list 之 vector 詞 轉換成 平均詞向量存回mongodb (左邊填入db.collection名稱,右邊填入使用之模型)