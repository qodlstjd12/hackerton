from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils import timezone  # pub_date를 위해 import
from django.contrib import auth

def login_view(request):
    if request.method == 'POST':
        username = request.POST["userid"]
        password = request.POST["userpw"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'Login.html', {'error': "username or passowrd is incorrect"})
    else:
        return render(request, 'Login.html')

def home(request):
    return render(request, 'main.html')

def mypage(request):
    return render(request, 'mypage.html')

def SignUp(request):
    return render(request, 'SignUp.html')