from user_info import verifing
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils import timezone  # pub_date를 위해 import
from django.contrib import auth
from .models import UserInfo, CustomUser, whodonate, Post1
from .form import PostForm
from .GoogleApi import google_api
from list.models import Post
from django.views.decorators.csrf import csrf_exempt
from .verifing import ggoo
import os

def home(request):
    msg =""
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'msg': msg})
    real_user = UserInfo.objects.get(user_email=request.user.email)   
    return render(request, 'index.html', {'msg':msg, 'qua':str(real_user.qua)})

def login_view(request):
    if request.method == 'POST':
        username = request.POST["userid"]
        password = request.POST["userpw"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('user_info:home')
        else:
            msg = "error"
            return render(request, 'login.html', {'msg':msg})
    else:
        return render(request, 'login.html')

@csrf_exempt
def signup(request):
    if request.method == "POST":
        
        try:
            if CustomUser.objects.get(email=request.POST['user_email']):
                return render(request, 'signup.html', {"error" : "error"})
        except:
            pass
        
        if request.POST["user_pw1"] == request.POST["user_pw2"]:
            user = CustomUser.objects.create_user(
                email=request.POST['user_email'], password=request.POST['user_pw1'])
            auth.login(request, user)
            user_contents = UserInfo()
            user_contents.user_email = request.POST['user_email']
            user_contents.user_nickname = request.POST['user_nickname']
            user_contents.user_phone = request.POST['user_num']
            user_contents.user_name = request.POST['user_name']
            user_contents.user_account = request.POST['user_acname']
            user_contents.user_account_name = request.POST['user_acnum']
            user_contents.save()
            return render(request, 'index.html')
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def verify(request):
    if request.method=='POST':
        img = request.FILES.get('image').read()
        user = CustomUser.objects.get(email=request.user)
        real_user = UserInfo.objects.get(user_email=request.user.email)
        msg = ""
        if ggoo(img,real_user.user_name):
            real_user.qua = 'yes'
            real_user.save()
            msg = "success"
        else:
            msg = "fail"
    return render(request, 'index.html', {'msg':msg})

def logout_view(request):
    auth.logout(request)
    return redirect('user_info:home')

def mypage(request):
    if not request.user.is_authenticated:
        msg = "Do Login"
        return render(request, "mypage.html", {'msg':msg})
    user = CustomUser.objects.get(email=request.user.email)
    userinfo = UserInfo.objects.get(user_email=user)
    #돈을 준 사람이 현재 유저인 사람과 같을때, 그니까 현재 유저한테 후원받은사람들 필터링
    my_donate_relation = whodonate.objects.filter(whogivemoney=request.user.email)
    #거기서 중복 제거
    mdr = my_donate_relation.values_list('whogetmoney', flat=True).distinct()
    my_receiver = []
    msg = ""
    for m in mdr:
        my_receiver.append(UserInfo.objects.get(user_email=m))


    if userinfo.qua == "yes":
        return redirect('user_info:sponserpage')
    if request.method == 'POST':
        money = request.POST['mine']
        try:
            money = int(money)
        except:
            msg = "failed"
            return render(request, 'mypage.html', {"error" : msg})

        save_money = int(userinfo.cash)
        userinfo.cash = money + save_money
        userinfo.user_totalcash += money
        userinfo.save()
        msg = "success"
    return render(request, 'mypage.html', {"userinfo" : userinfo ,"money" : userinfo.cash,"success":msg ,'receivers':my_receiver ,"temperature" : str(round(0.1 * (userinfo.user_totaldonate / 1000),2))})

def recentDetail(request, id):
    post = Post1.objects.get(id=id)
    return render(request, 'recentDetail.html', {'post':post})

def recentWrite(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.post_time = timezone.now()
            post.photo=request.FILES.get('image')
            if str(post.photo) == "":
                post.photo = None
                path = []
            else:
                path = str(post.photo.path).split('\\')

            post.save()
            if path!=[]:
                t_path  = ''
            
                for i in path:
                    if i == 'media':
                        t_path = t_path + i + '\\' + 'userinfo' + '\\'
                    elif i.find('jpg') != -1 :
                        t_path = t_path + i
                    else:    
                        t_path = t_path + i + '\\'
                if google_api(t_path):
                    return redirect('user_info:sponserpage')
                else:
                    post.delete()
                    os.remove(t_path)
                path = ""
                return render(request, 'recentWrite.html', {"error" : "error"})
        return redirect('user_info:sponserpage')
    return render(request, 'recentWrite.html')

def recentWriteUpdate(request, id):
    pass

from django.core.paginator import Paginator

def sponserpage(request):
    user = CustomUser.objects.get(email=request.user.email)
    whos = whodonate.objects.filter(whogetmoney=user)
    posts = Post.objects.filter(writer=request.user)
    paginator = Paginator(posts, 8)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    user_profile = UserInfo.objects.get(user_email = request.user)
    recent_posts = Post1.objects.filter(writer=request.user).order_by('-post_time')
    recent_paginator = Paginator(recent_posts, 8)
    recent_page = request.GET.get('page')
    recent_posts = recent_paginator.get_page(recent_page)

    return render(request, 'sponserpage.html', {'whos' : whos, 'posts': posts, 'recent_posts':recent_posts , 'user_profile':user_profile})

def recentView(request, email):
    user = CustomUser.objects.get(email=email)
    userinfo = UserInfo.objects.get(user_email = email)
    posts = Post1.objects.filter(writer=user).order_by('post_time')

    return render(request, 'recentView.html', {'posts': posts, 'receiver' : userinfo})

def profile_view(request):
    user_profile = UserInfo.objects.get(user_email = request.user)
    return render(request, "profile.html", {"user_profile" : user_profile})

def profile_update_view(request):
    if request.method == 'POST':
        user_profile = UserInfo.objects.get(user_email = request.user)
        user_profile.user_description = request.POST['user_description']
        try: 
            user_profile.user_image.path 
            os.remove(user_profile.user_image.path)
        except:
            pass
        user_profile.user_image = request.FILES.get('image')
        user_profile.save()
        return redirect("user_info:mypage")
    return render(request, "profile.html")

