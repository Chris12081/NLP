import string
# rdata = open('.ipynb_checkpoints/tra_list_ing_all2.txt','r',encoding='utf-8',errors='ignore')
# first_line = rdata.readline()
# print(first_line)

abc = {}
rdata = open('tra_mydict.txt','r',encoding='utf-8',errors='ignore')
data = rdata.readlines()
for each in data:
    abc[each.strip('\n')] = 0
print(abc)
print(data)
print(string.punctuation)