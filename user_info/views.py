from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils import timezone  # pub_date를 위해 import
from django.contrib import auth
from .models import UserInfo, CustomUser



def home(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST["userid"]
        password = request.POST["userpw"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('user_info:home')
        else:
            return render(request, 'login.html', {'error': "username or passowrd is incorrect"})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        if request.POST["user_pw1"] == request.POST["user_pw2"]:
            user = CustomUser.objects.create_user(
                email=request.POST['user_email'], password=request.POST['user_pw1'])
            auth.login(request, user)
            user_contents = UserInfo()
            user_contents.user_email = request.POST['user_email']
            user_contents.user_phone = request.POST['user_num']
            user_contents.user_name = request.POST['user_name']
            user_contents.user_account = request.POST['user_acname']
            user_contents.user_account_name = request.POST['user_acnum']
            user_contents.save()
            return redirect('user_info:home')
        return render(request, 'signup.html')
    return render(request, 'signup.html')



def logout_view(request):
    auth.logout(request)
    return redirect('user_info:home')

def mypage(request):
    if request.method == 'POST':
        money = request.POST['mine']
        try:
            money = int(money)
        except:
            return render(request, 'mypage.html', {"error" : "failed"})
        user = CustomUser.objects.get(email=request.user.email)
        userinfo = UserInfo.objects.get(user_email=user)
        try:
            save_money = int(userinfo.cash)
            print(save_money)
            print(money)
            userinfo.cash = money + save_money
        except:
            userinfo.cash = money
        userinfo.save()
        return render(request, 'mypage.html', {"money" : userinfo.cash})
       

    return render(request, 'mypage.html')