from django.shortcuts import render, redirect
from django.contrib import auth
from .models import Author, Book, UserBook, Memo
from accounts.models import Profile
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re
from django.http import JsonResponse
import os
import sys
import json

# Create your views here.

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
        p=re.compile('<b>|</b>')
        book_title=p.sub('',dict["items"][0]["title"])
        book_title=re.search('.+(?=\()',book_title)
        book_author=dict["items"][num]["author"]
        title_author=[book_title,book_author]
        return title_author

    else:
        print("Error Code:" + rescode)

def get_page(title,num):
    baseUrl = 'https://book.naver.com/search/search.nhn?sm=sta_hty.book&sug=&where=nexearch&query='

    url = baseUrl + quote_plus(title) #네이버 책 홈에서 책 제목을 검색해서 나오는 url
    html = urllib.request.urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")

    site_for_page = bsObject.select('li > dl > dt > a') # 책 제목을 검색해서 뜨는 a 태그들 결과들의 링크

    deturl=site_for_page[num].attrs['href'] # 페이지 수가 써있는 url로 들어옴 index 0으로 한 건 편의를 위함, 추후 바뀔 수 있음

    html=urllib.request.urlopen(deturl)
    bs=BeautifulSoup(html, "html.parser")

    whole_page= bs.select('.book_info_inner') 

    m=re.search('페이지.\d+',whole_page[0].text)
    #n=re.search('저자.(\w+|\s|\.)+',whole_page[0].text)

    page=re.search('\d+',m.group())
    #author=re.search('(?!저)(?!자)(?!\s)(\w+|\s|\.)+',n.group()) #정규식 앞에 '저자 ' 제거하는 방법이 있을 거 같은데...
    
    #page_author=[page.group(),author.group()]
    return int(page.group())

def index(request):
    if request.method=='POST':
        member=request.user.profile 
        ta_list=search_title_author(request.POST['title'],0)
        book_title=ta_list[0]
        book_author=ta_list[1]
        
        #추가하려는 책의 작가가 이미 있는지 확인하고 없으면 추가
        try:
            is_author_in_list=Author.objects.get(name=book_author)

        except Author.DoesNotExist:
            Author.objects.create(name=book_author)
        
        bookauthor=Author.objects.get(name__iexact=book_author)
        #추가하려고 하는 책이 이미 있는지 확인하고 없으면 추가
        try:
            is_in_list=Book.objects.get(title__iexact=book_title, author=bookauthor)

        except Book.DoesNotExist:
            Book.objects.create(title=book_title, author=bookauthor)
        
        book= Book.objects.get(title__iexact=book_title, author=bookauthor)
        # 저장된 횟수 추가
        book.count+=1
        bookauthor.count+=1
        book.save()
        bookauthor.save()

        whole_page=get_page(book_title,0)
        member.already_read+=whole_page
        UserBook.objects.create(userid=member,bookid=book,whole_page=whole_page)
        
        return JsonResponse({"message":"created"},status=201)

    else: 
        if request.user.is_authenticated:
            member=request.user.profile
            books=UserBook.objects.filter(userid=member)
            authors=Author.objects.all()
            ratio=member.already_read/member.goal
            return render(request,'bookshelf/index.html',{"books":books,"authors":authors,"ratio":ratio})
        else:
            return render(request,'bookshelf/index.html')
    
def create_book(request):
    return render(request,'bookshelf/new.html')

def list_friends(request):
    follows=request.user.profile.follows
    return request(request,'index.html',{"follows":follows})

def delete_book(request,id):
    userbook=UserBook.objects.get(id=id)
    userbook.delete()
    return redirect('/bookshelf')

def show_memo(request,id):
    userbook=UserBook.objects.get(id=id)
    memos=Memo.objects.filter(book=userbook)
    memo_list=[]
    for i in memos:
        memo_list.append([i.page,i.content])
    memo_json=json.dumps(memo_list,ensure_ascii = False)

    context = {
        'title': userbook.bookid.title,
        'author':userbook.bookid.author.name,
        'memo_json':memo_json,
    }
    
    return JsonResponse(context)

def recommend_book(request):
    by_book=Book.objects.all().order_by('-count')
    best_author=Author.objects.all().order_by('-count').first()
    by_author=Book.objects.filter(author=best_author)#.exclude로 자기가 읽은 책 제외해야 함
    return render(request,'bookshelf/recommend.html',{"by_books":by_book,'by_author':by_author})

def create_memo(request,id):
    page=request.POST['page']
    content=request.POST['content']
    new_memo = Memo.objects.create(content=content, page=page,book_id=id )
    '''
    context = {
        # memo의 id도 필요할까?
        # memo 자체에 접근하려면 필요한데 삭제 말고 접근할 일이 없으니 일단 두기
        'page': new_memo.page,
        'content': new_memo.content,
        'create_at':new_memo.created_at
    }
    '''
    memos=Memo.objects.filter(book=userbook)
    memo_list=[]
    for i in memos:
        memo_list.append([i.page,i.created_at,i.content])
    memo_json=json.dumps(memo_list)

    context = {
        'title': userbook.bookid.title,
        'author':userbook.bookid.author.name,
        'memo_json':memo_json,
    }
    
    # return redirect('bookself/show.html')
    return JsonResponse(context)

def delete_memo(request,id,mid):
    m=Memo.objects.get(id=mid)
    m.delete()    
    return redirect('bookshelf/show.html')