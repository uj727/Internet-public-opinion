from chainer import collections
import pymssql
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from ckiptagger import data_utils, construct_dictionary, WS, POS
#data_utils.download_data_gdown(r'C:\Users\User\OneDrive\桌面\driver')
from ckiptagger import WS, POS, NER
ws = WS("./data")

push_list=[]
ex_list=[]
conn = pymssql.connect(server='LAPTOP-HK90694P', user='sa', password='az900727', database='pttstock',autocommit=True)  
cursor = conn.cursor()  
cursor.execute("SELECT MessageContent \
                from Message\
                where MessageLike='推'")
conn.commit()
row = cursor.fetchone()  
while row:    
    print("["+row[0]+"]")
    push_list.append(''.join(row[0]))
    row = cursor.fetchone()      
row = cursor.fetchone()  
#切字
pushws_results = ws(push_list)
print(pushws_results)
#分
push_str=""
for i in pushws_results:
    push_str+='\t\t'.join([ii.replace(" ","")for ii in i])
    push_str+='\t\t'
push=push_str.replace("了\t\t","")
push=push.replace("的\t\t","")
print(push)

wo = WordCloud(font_path=r'C:\Windows\Fonts\mingliu.ttc', width=1200, height=800, margin=2).generate(push)
plt.imshow(wo,interpolation='bilinear')
plt.axis("off")
plt.show()
print(push)
print("-------------------------------------------------------------------------------------------------------")

cursor.execute("SELECT MessageContent \
                from Message\
                where MessageLike='噓'")
conn.commit()
row = cursor.fetchone() 

while row:    
    ex_list.append("".join(row[0]))
    row = cursor.fetchone()  
exws_results = ws(ex_list)
print(exws_results)  

ex_str=""
for i in exws_results:
    ex_str+='\t\t'.join([ii.replace(" ","")for ii in i])
    ex_str+='\t\t'
print(ex_str)      

ex=ex_str.replace("了\t\t","")
ex=ex.replace("的\t\t","")

wcl=WordCloud(background_color="white",font_path=r'C:\Windows\Fonts\mingliu.ttc',width=1200,height=800,margin=2).generate(ex)
plt.imshow(wcl,interpolation='bilinear')
plt.axis("off")
plt.show()

