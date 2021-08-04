from django.shortcuts import render
from .models import Post1
from .forms import PostForm
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.models import User
from user_info.models import UserInfo, CustomUser

def FAQ(request):
    try:
        user = CustomUser.objects.get(email=request.user.email)
    except:
        return render(request, 'FAQ.html')
        
    post1 = Post1.objects.filter(writer=user) # 내가 쓴글만
    return render(request, 'FAQ.html', {'post1': post1})


def CS(request):
    if request.method == 'POST':
        post1 = Post1()
        post1.title = request.POST['title']
        post1.body = request.POST['body']
        post1.writer = CustomUser.objects.get(email=request.user.email)
        post1.post_time = str(timezone.now())[0:19]
        post1.save()
        return redirect('user_info:home')
    else:
        form = PostForm()
        return render(request, 'CS.html',{'post':form})