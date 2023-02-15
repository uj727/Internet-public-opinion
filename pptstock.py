import pymssql 
import requests
from bs4 import BeautifulSoup  
import random
import time
import csv 

conn = pymssql.connect(server='LAPTOP-HK90694P', user='sa', password='az900727', database='pttstock',autocommit=True)  
cursor = conn.cursor()  
 
user_agent_lis = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"]
my_user_agent = random.choice(user_agent_lis)
url="https://www.ptt.cc/bbs/Stock/index4964.html"
my_headers = {'User-Agent': my_user_agent}

def write_csv(list_row):
	with open ('1081649.csv','a+',newline='\n') as csvfiles:
		writer =csv.writer(csvfiles)
		writer.writerow(list_row)
	csvfiles.close()
title_list=[]

#輸出有空格
Dstr=' 1/16'
#換頁 ex 4965~4966
for page in range(0,4):
    r = requests.get(url, headers=my_headers)
    soup = BeautifulSoup(r.text,"html.parser")    
    btn = soup.select('div.btn-group a')#下一頁按鈕
    #在bottunGroup第5個位置
    up_page_href = btn[4]['href']
   # print(up_page_href)
    next_page_url = 'https://www.ptt.cc' + up_page_href
    url= next_page_url

 
    target = soup.select('div.r-ent')
    #抓日期時間
    for item in target:
            date = item.select_one('div.date')
            #print('['+date.string+']')
            #16號就抓文章網址
            time.sleep(1)
            if(date.string == Dstr):
                href = item.select_one('div.title a').get('href')
                
                #爬文章內容 先替換url
                url='https://www.ptt.cc'+href
                r = requests.get(url, headers=my_headers)
                soup = BeautifulSoup(r.text,"html.parser")
               
                ## 查找所有html 元素 抓出內容         
                main_container = soup.find(id='main-container')
                context = main_container.text
                #  以"-- " 切割成2個陣列 把評論切掉
                context = context.split('※ 發信站')[0]
                    
                # 把每段文字 '\n' 去除
                context = context.split('\n')
                # 去頭留內容 
                contents = context[2:]
                # 內容轉string
                content = '\n'.join(contents)

                artical = soup.select('span.article-meta-value')
                # 作者
                author = artical[0].text
                # stock版
                board = artical[1].text
                # 文章標題
                title = artical[2].text
                # 日期
                date = artical[3].text
                print('作者 '+author)
                print('看板 '+board)
                print('標題 '+title)
                print('日期 '+date) 
                print('內容'+content)     
                cursor.execute("Insert into ARTICLE\
                 (ArticleCommunity,AuthorName,DateTime,ArticleTitle,ArticleContent)Values\
                    ('"+board+"','"+author+"','"+date+"','"+title+"','"+content+"')")
                conn.commit()
                time.sleep(2)
                cursor.execute("SELECT ArticleID,ArticleTitle\
                FROM Article\
                WHERE ArticleTitle = '"+title+"'")
                row = cursor.fetchone()  
                while row:  
                    print (row[0],row[1])  
                       
                    id=str(row[0])
                    row = cursor.fetchone()
                
                #推噓 人 留言
                message = soup.find_all('div', 'push')   
                for item in message:
                    push=item.find('span','push-tag').getText()
                    user=item.find('span','push-userid').getText()
                    mes=item.find('span','push-content').getText().replace("'", "").replace("’", "").replace(":", "").replace(" ", "")
                    mtime=item.find('span','push-ipdatetime').getText()
                    print(push)
                    # print(user)
                    print(mes)
                    # print(mtime)
                    print("----------------")
                    cursor.execute("Insert into MESSAGE\
    (ArticleID,AuthorMessage,mTime,MessageContent,MessageLike)Values\
        ('"+id+"','"+user+"','"+mtime+"','"+mes+"','"+push+"')")
                    conn.commit()
            url = next_page_url
    print(url)           
conn.close()
  
           
        
        






