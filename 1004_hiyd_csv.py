


import pandas as pd
import pymongo
import jieba
import re
from IPython.display import clear_output
clear_output(wait=True)
pd.set_option('display.max_columns', 110)

jieba.load_userdict('./jieba_sport/mydict.txt')
# Create connnect 建立與mongoDB連線
client = pymongo.MongoClient(host='192.168.158.128', port=27017)
# assign database 選擇資料庫
db = client.tibame
# assign colection 選擇collection
collection = db.hiyd

# 利用pd.DataFrame 查看表格
data = pd.DataFrame(list(collection.find()))
# print(data)

# Query specific column from all hiyd_raw 選擇要讀取的資料欄位
queryArgs = {}
projectField = {'url' : True, 'title' : True, 'lesson_time' : True,'strengh' : True}
# 資料庫記得調整
search_response = db.hiyd.find(queryArgs, projection=projectField)
sport_list = []
for item in search_response:
    sport_list.append(item)
# print(sport_list[2]['url'])

x_list = ['lesson_time','strengh']
def rep(x):
    for i in range(288):
        sport_list[i][x]=re.sub('[^\d]','',sport_list[i][x])
if __name__ == '__main__':
    for x in x_list:
        rep(x)
# print(sport_list)

# 保留字
reserve_words_list = []
with open(file='./jieba_sport/mydict2.txt',mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        reserve_words_list.append(line)
# print(reserve_words_list)
# 針對 title 斷詞
n = 0
for i in range(288): #288
    ti = jieba.lcut(sport_list[i]['title'], cut_all=False)
    # print('精確模式: ',ti)

    # 取斷詞 與 保留字 交集 留下key word
    matched = set(ti).intersection(set(reserve_words_list))
    match = list(matched)
    try:
        print('keyword: ',match[0])
        # 將keyword 轉換為 title
        sport_list[i]['title'] = match[0]
        print(n)
        n += 1

    except IndexError:
        sport_list[i]['title'] = 0
# 寫入csv
name_attribute = ['url','title','lesson_time','strengh']
writerCSV = pd.DataFrame(columns=name_attribute,data = sport_list)
writerCSV.to_csv('./hiyd_clean.csv',sep=',',encoding='cp950')
# 再將 CSV 透過txt 轉成 utf-8   title 類別修改成 text 即可匯入mysql
