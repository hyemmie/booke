from django.shortcuts import render, redirect
#from django.contrib import auth
from .models import Author, Book, UserBook, Memo
from accounts.models import Profile, Follow
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re
from django.http import JsonResponse
import os
import sys
import json
from django.core.serializers import serialize 

# Create your views here.

def search_title_author_image(title,num):
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
        book_title=p.sub('',dict["items"][num]["title"])
        while book_title.find('(')!=-1:
            book_title=re.search('.+(?=\()',book_title).group()
        book_author=dict["items"][num]["author"]
        book_image=dict["items"][num]["image"]
        display=dict["display"]
        title_author_image=[book_title,book_author,book_image,display]
        return title_author_image

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
    page=re.search('\d+',m.group())

    return int(page.group())

def index(request):    
    if request.method=='POST':
        member=request.user.profile
        ta_list=search_title_author_image(request.POST['title'],0)
        book_title=ta_list[0]
        book_author=ta_list[1]
        book_image=ta_list[2]
        color=request.POST['color']
        
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
            Book.objects.create(title=book_title, author=bookauthor,image=book_image)
        
        book= Book.objects.get(title__iexact=book_title, author=bookauthor)
        # 저장된 횟수 추가
        book.count+=1
        bookauthor.count+=1
        book.save()
        bookauthor.save()

        whole_page=get_page(book_title,0)
        member.already+=whole_page
        member.save()
        UserBook.objects.create(userid=member,bookid=book,whole_page=whole_page,color=color)
        # new_book = UserBook.objects.latest('id')

        # res = {
        #     'id':new_book.id,
        # }
        
        return JsonResponse({"message":"created"},status=201)

    else:        
        if request.user.is_authenticated:
            member=request.user.profile
            books=UserBook.objects.filter(userid=member)
            authors=Author.objects.all()
            page=0
            count=0
            list1=[]
            list2=[]
            list3=[]
            list4=[]
            list5=[]
            for bo in books:
                page+=bo.whole_page
                if page<=2000:
                    if count==0: list1.append(bo.id)
                    elif count==1: list2.append(bo.id)
                    elif count==2: list3.append(bo.id)
                    elif count==3: list4.append(bo.id)
                    elif count==4: list5.append(bo.id)
                else:
                    page=bo.whole_page
                    count+=1
                    if count==0: list1.append(bo.id)
                    elif count==1: list2.append(bo.id)
                    elif count==2: list3.append(bo.id)
                    elif count==3: list4.append(bo.id)
                    elif count==4: list5.append(bo.id)
            ub1=UserBook.objects.filter(id__in=list1)
            ub2=UserBook.objects.filter(id__in=list2)
            ub3=UserBook.objects.filter(id__in=list3)
            ub4=UserBook.objects.filter(id__in=list4)
            ub5=UserBook.objects.filter(id__in=list5)

            # follow도 index get일 때 같이 처리
            follows=Follow.objects.filter(followed_by=request.user.profile)
            id_list=[person.id for person in follows]
            follow_list=Profile.objects.filter(id__in=id_list)
            res_follows=list(follow_list.values('nickname','id'))

            return render(request,'bookshelf/index.html',{"books":books,"authors":authors,"follows":res_follows,"ub1":ub1,"ub2":ub2,"ub3":ub3,"ub4":ub4,"ub5":ub5})
        else:
            return render(request,'bookshelf/index.html')
            

def create_book(request):
    return render(request,'bookshelf/new.html')

# def list_friends(request):
#     follows=Follow.objects.filter(followed_by=request.user.profile)
#     print(type(follows))
#     id_list=[person.id for person in follows]
#     follow_list=Profile.objects.filter(id__in=id_list)
#     res_follows=list(follow_list.values('nickname','id'))

#     context = {
#         'follows':res_follows
#     }
    
#     print(context)
#     return JsonResponse(context)


def delete_book(request,id):
    userbook=UserBook.objects.get(id=id)
    userbook.delete()
    userp=request.user.profile
    userp.already-=userbook.whole_page  
    userp.save()  
    context={
        'id':userbook.id,
    }
    return JsonResponse(context)

def recommend_book(request):
    if Book.objects.count()>=5:
        by_book=Book.objects.all().order_by('-count')[:5]
    else :
        by_book=Book.objects.all().order_by('-count')
    best_author=Author.objects.all().order_by('-count').first()
    by_author=[]
    image=[]
    author=[]
    for_author=search_title_author_image(best_author.name,0)
    for i in range(for_author[3]):
        rec=search_title_author_image(best_author.name,i)
        by_author.append(Book.objects.create(title=rec[0],author=best_author,image=rec[2]))  

    return render(request,'bookshelf/recommend.html',{"by_books":by_book,'by_author':by_author})

def show_memo(request,id):
    userbook=UserBook.objects.get(id=id)
    memo_data=list(Memo.objects.filter(book=userbook).values('id','book','content','page'))

    context = {
        'userbook': {
            'title':userbook.bookid.title,
            'author':userbook.bookid.author.name,
            'id':userbook.id,
        }, 
        'memos': memo_data,

    }

    return JsonResponse(context)
    
    #context=json.dumps(context,ensure_ascii=False)
    # return redirect('bookshelf/show.html',{"userbook":userbook,"memos":memos})
    # return JsonResponse({"message" : "created"}, status=201)
    # return redirect("/bookshelf/%d/" %id)
    # return render(request, 'bookshelf/show.html', {'userbook': userbook, 'memos':memos})
    #return JsonResponse(context)

def create_memo(request,id):
    if request.method=='POST':
        userbook=UserBook.objects.get(id=id)
        page=request.POST['page']
        content=request.POST['content']
        new_memo=Memo.objects.create(content=content, page=page, book_id=id )
        memo_data = list(Memo.objects.filter(book=userbook).values('id', 'book', 'content','page') )        
        
        context = {
            'new_memo_id':new_memo.id,
            'page': new_memo.page,
            'content': new_memo.content,
            'userbook': {
            'title':userbook.bookid.title,
            'author':userbook.bookid.author.name,
            'id':userbook.id,
            }, 
            #'memos': memo_data,
        }

        # return redirect('bookself/show.html')
        return JsonResponse(context)

    elif request.method=='GET':
        userbook=UserBook.objects.get(id=id)
        memos=Memo.objects.filter(book=userbook)

    return render(request,'bookshelf/show.html',{"userbook":userbook,"memos":memos})
    # return render(request,'#showModal',{"userbook":userbook,"memos":memos})
    

def delete_memo(request,bid,mid):
    m=Memo.objects.get(id=mid)
    m.delete()    
    return JsonResponse({"message":"created"},status=201)

def friends_shelf(request,id):
    member=Profile.objects.get(user_id=id)
    print(member)
    books=UserBook.objects.filter(userid=member)
    authors=Author.objects.all()
    page=0
    list1=list2=list3=list4=list5=[]
    for bo in books:
        page+=bo.whole_page
        if page<=2000:
            list1.append(bo.id)
        elif page<=4000:
            list2.append(bo.id)
        elif page<=6000:
            list3.append(bo.id)
        elif page<=8000:
            list4.append(bo.id)
        else:
            list5.append(bo.id)
    ub1=UserBook.objects.filter(id__in=list1)
    ub2=UserBook.objects.filter(id__in=list2)
    ub3=UserBook.objects.filter(id__in=list3)
    ub4=UserBook.objects.filter(id__in=list4)
    ub5=UserBook.objects.filter(id__in=list5)

    follows=Follow.objects.filter(followed_by=request.user.profile)
    id_list=[person.id for person in follows]
    follow_list=Profile.objects.filter(id__in=id_list)
    res_follows=list(follow_list.values('nickname','id'))

    return render(request,'bookshelf/friends.html',{"friend":member,"books":books,"authors":authors,"follows":res_follows,"ub1":ub1,"ub2":ub2,"ub3":ub3,"ub4":ub4,"ub5":ub5}) 
