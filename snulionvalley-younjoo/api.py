import os
import sys
from bs4 import BeautifulSoup
import urllib.request
import json
import re


def search_book(title):
    client_id = "4dDEAG4leXp6OiKVgE7G" 
    client_secret = "gw8Luw9s2F"
    encText = urllib.parse.quote(title)    
    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText #+"&display=3&sort=sim" 뒤에 붙는 건 검색결과는 3개만, 정렬방법: 유사도라는 ㅣ뜻
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)

    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print (type(response_body.decode('utf-8')))
        print(response_body.decode('utf-8'))
        dict=json.loads(response_body.decode('utf-8'))
        print(dict["items"][0]["author"])
        print (type(dict["items"][0]["author"]))
            #print(item["title"]+" "+item["author"])
        print(re.search('(?!b)(\w+|\s|,)+',dict["items"][0]["title"]).group())

    else:
        print("Error Code:" + rescode)

def search_title_author(title,num):
    client_id = "4dDEAG4leXp6OiKVgE7G" 
    client_secret = "gw8Luw9s2F"
    encText = urllib.parse.quote(title)    
    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText #+"&display=3&sort=sim" 뒤에 붙는 건 검색결과는 3개만, 정렬방법: 유사도라는 ㅣ뜻
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)

    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        dict=json.loads(response_body.decode('utf-8'))
        #book_title=re.search('(?!b)(\w+|\s|,)+',dict["items"][0]["title"]).group()
        p=re.compile('<b>|</b>')
        book_title=p.sub('',dict["items"][0]["title"])
        while book_title.find('(')!=-1:
            book_title=re.search('.+(?=\()',book_title).group()
            
        print(book_title)
        print (dict["items"][0]["title"])
        book_author=dict["items"][num]["author"]
        print(book_author)
        title_author=[book_title,book_author]
        
        return title_author
    else:
        print("Error Code:" + rescode)

search_title_author("변신",0)
context = {
        'userbook':{
            'title': '변신',
            'author':'프란츠 카프카',
        },
        'memo_list':[[200,'재밌어요']],
    }

print(context['memo_list'])
print (json.dumps(context,ensure_ascii=False))
