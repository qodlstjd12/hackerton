from datetime import time
from django.http.response import HttpResponse
from .models import Post, Photo
from .forms import PostForm
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def list_view(request):
    post = Post.objects.all()
    return render(request, 'html/feed.html', {'posts':post})

@csrf_exempt
def helpWrite(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        post.writer= request.user
        post.post_time = timezone.now()
        post.body = request.POST.get('body')
        post.thumbnail = request.FILES.get('images')
        post.save()
        return redirect('list:list_view')
    else:
        form = PostForm()
        return render(request, 'html/helpWrite.html', {'post':form})

def feed_Detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'html/feedDetail.html', {'post':post})


def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('list:list_view')

def ask(request):
    return render(request, 'html/ask.html')

def feed(request):
    return render(request, 'html/feed.html')

def recentview(request):
    return render(request, 'html/recentView.html')

def recentWrite(request):
    return render(request, 'html/recentWrite.html')
