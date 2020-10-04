import pandas as pd
import numpy as np
import csv
pd.set_option('display.max_columns', 110)

# 讀取 nutrient
nutrient_df = pd.read_csv('nutrients_2019_0926.csv',encoding='utf-8')
# print(nutrient_df)

# Filling NA with 0's

nutrient_df = nutrient_df.iloc[:54,:].fillna(0)
# print(nutrient_df)

# Make all stats in the same per-unit scale
# 把礦物質 單位從 mg 變為g
nutrient_df['minerals'] = nutrient_df['minerals'] / 1000
# print(nutrient_df)

# 把 vitamina A turn IU to g
nutrient_df['vitamina'] = nutrient_df['vitamina'] * 0.0000003
# print(nutrient_df)

#Vitamina B,C,E從mg變成g
nutrient_df['vitaminb'] = nutrient_df['vitaminb'] /1000
nutrient_df['vitaminc'] = nutrient_df['vitaminc'] /1000
nutrient_df['vitamine'] = nutrient_df['vitamine'] /1000
nutrient_df['cholesterol'] = nutrient_df['cholesterol'] /1000
# print(nutrient_df)

# 將營養成分統計表的食材對應到我們定義的保留食材項目
with open ('./jieba_data/mydict.txt','r',encoding='utf-8') as f:
    txt = f.readlines()
    word_bank = [element.replace(' 10 n','').replace(' 20 n','').strip('\n') for element in txt]

# print(word_bank[:-8])

nutrient_df['fname']  = word_bank[:-8]
print(nutrient_df)

# nutrient_df.to_csv('./nutrients.csv', sep=',',encoding='utf-8')