import re
from django.core.exceptions import PermissionDenied, ValidationError
from user_info import verifing
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone  # pub_date를 위해 import
from django.contrib import auth, messages
from .models import UserInfo, CustomUser, whodonate, Post1
from .forms import CustomSetPasswordForm, PostForm, RecoveryPwForm
from .GoogleApi import google_api
from list.models import Post
from django.views.decorators.csrf import csrf_exempt
from .verifing import ggoo


from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator

import os

def home(request):
    msg =""
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'msg': msg})
    real_user = UserInfo.objects.get(user_email=request.user.email)   
    return render(request, 'index.html', {'msg':msg, 'qua':str(real_user.qua)})

def findID(request):
    msg = ""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        try:
            user = UserInfo.objects.get(user_phone = phone)
            msg = user.user_email
        except:
            msg = "error"
        return render(request, 'findID.html', {'msg':msg})
    return render(request, 'findID.html')


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
        msg =""
        return render(request, 'login.html', {'msg':msg})

@csrf_exempt
def signup(request):
    msg =""
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
            msg = "signup_success_but_email"
            return render(request, 'index.html', {'msg': msg})
        msg = "NOTSAME_PW"
        return render(request, 'signup.html', {'msg':msg})
    return render(request, 'signup.html')

def delete(request):
    user = CustomUser.objects.get(email=request.user.email)
    user_info = UserInfo.objects.get(user_email = user.email)
    auth.logout(request)
    user_info.delete()
    user.delete()
    msg = "delete_success"
    return render(request, 'index.html', {'msg':msg})

def get_success_url(request):
    msg="sending"
    user = UserInfo.objects.get(user_email=request.user.email)
    send_mail(
        '[WhoWant] {}님의 회원가입 인증메일 입니다.'.format(user.user_name),
            [user.user_email],
            html=render_to_string('register_email.html', {
                'user': request.user,
                'uid': urlsafe_base64_encode(force_bytes(request.user)).encode().decode(),
                'domain': request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(request.user),
            }),
    )
    return render(request, 'index.html', {'msg':msg})
#유저 메일 활성화
def activate(request, uid64, token):
    msg = ""
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        print(uid)
        current_user = CustomUser.objects.get(email=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        msg = "activate_error"
        return render(request, 'index.html', {'msg': msg})
    msg = "token_error"
    if default_token_generator.check_token(current_user, token):
        current_user.active = True
        current_user.save()
        msg = "email_success"
    return render(request, 'index.html', {'msg': msg})

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
            image = request.FILES.get('image')
            
            if image:
                img = request.FILES.get('image').read()
                if google_api(img):
                    post.photo=image
                    post.save()
                    return redirect('user_info:sponserpage')
                else:
                    return render(request, 'recentWrite.html', {"error" : "error"})
        post.save()
        return redirect('user_info:sponserpage')
    return render(request, 'recentWrite.html')

def recentWriteUpdate(request, id):
    post = Post1.objects.get(id=id)
    whos = whodonate.objects.filter(whogetmoney=request.user)
    posts = Post.objects.filter(writer=request.user).order_by('-post_time')
    recent_posts = Post1.objects.filter(writer=request.user).order_by('-post_time')
    user_profile = UserInfo.objects.get(user_email = request.user)
    msg = ""
    if request.method == 'POST':
        post.title = request.POST['title']
        post.body = request.POST['body']
        image = request.FILES.get('image')
        if image:
            img = request.FILES.get('image').read()
            if google_api(img):
                post.photo=image
                post.save()
                return redirect('user_info:sponserpage')
            else:          
                return render(request, 'recentWrite.html', {"error" : "error"})
        post.save()
        msg = "update_success"
        return render(request, 'sponserpage.html', {'whos' : whos, 'posts': posts, 'recent_posts':recent_posts , 'user_profile':user_profile, 'msg':msg})
    return render(request, 'recentWriteUpdate.html', {'post':post})

def recentDelete(request, id):
    post = Post1.objects.get(id=id)
    post.delete()
    return redirect('user_info:sponserpage')
from django.core.paginator import Paginator

def spon_delete(request):
    user = CustomUser.objects.get(email = request.user.email)
    whos = whodonate.objects.filter(whogetmoney=user)
    user_info = UserInfo.objects.get(user_email=request.user.email)
    for who in whos:
        who.delete()
    auth.logout(request)
    user_info.delete()
    user.delete()
    msg = 'spon_delete'
    return render(request, 'index.html', {'msg':msg})

def sponserpage(request):
    msg = ""
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

    return render(request, 'sponserpage.html', {'whos' : whos, 'posts': posts, 'recent_posts':recent_posts , 'user_profile':user_profile, 'msg':msg})

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

from django.views.generic import View
class RecoveryPwView(View):
    template_name = 'recovery_pw.html'
    recovery_pw = RecoveryPwForm
    
    def get(self, request):
        if request.method == 'GET':
            form = self.recovery_pw(None)
            return render(request, self.template_name, {'form_pw': form})

from .helper import email_auth_num, send_mail
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
import json

def ajax_find_pw_view(request):
    email = request.POST.get('email')
    print(email)
    target_user = CustomUser.objects.get(email = email)
    print(target_user.email)
    if target_user:
        auth_num = email_auth_num()
        target_user.auth = auth_num
        print(target_user.auth)
        target_user.save()

        send_mail(
            '[WhoWant] 비밀번호 찾기 인증메일입니다.',
            [email],
            html=render_to_string('recovery_email.html',{
                'auth_num' : auth_num,
            }),
        )
    return HttpResponse(json.dumps({"result": target_user.email}, cls=DjangoJSONEncoder), content_type = "application/json")

def auth_confirm_view(request):
    print('여기')
    user_email = request.POST.get('email')
    print(user_email)
    input_auth_num = request.POST.get('input_auth_num')
    print(input_auth_num)
    target_user = CustomUser.objects.get(email=user_email, auth=input_auth_num)
    target_user.auth=""
    target_user.save()
    print(1)
    request.session['auth'] = target_user.email

    return HttpResponse(json.dumps({"result": target_user.email}, cls=DjangoJSONEncoder), content_type = "application/json")

def auth_pw_reset_view(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied
    
    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = CustomUser.objects.get(email = session_user)

        auth.login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)

        if reset_password_form.is_valid():
            user = reset_password_form.save()
            msg = "success"
            auth.logout(request)
            return render(request, 'login.html', {'msg': msg})
        else:
            auth.logout(request)
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)
    return render(request, 'password_reset.html', {'form':reset_password_form})