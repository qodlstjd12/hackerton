from user_info.models import CustomUser, UserInfo
from django.core import paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import MarketPost, Comment
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

def market_view(request):
    post = MarketPost.objects.all().order_by('-id')
    paginator = Paginator(post, 3)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    return render(request, 'market.html', {'posts':post})

from django.shortcuts import get_object_or_404

def market_Detail(request,id):
    post = MarketPost.objects.get(id=id)
    user_info = UserInfo.objects.get(user_email = request.user)
    
    try:
        comments = Comment.objects.get(id=id) 
    except:
        comments = None

    return render(request, 'marketDetail.html', {"comments":comments, 'post':post, "user_info" : user_info})

@csrf_exempt
def market_Write(request):
    if request.method == 'POST':
        post = MarketPost()
        post.title = request.POST.get('title')
        print(request.user)
        post.writer = request.user
        post.post_time = timezone.now()
        post.body = request.POST.get('body')
        post.thumbnail = request.FILES.get('image')
        post.save()
        return redirect('market:market_view')
    return render(request, 'marketWrite.html')

def market_Delete(request, id):
    post = MarketPost.objects.get(id=id)
    post.delete()
    return redirect('market:market_view')

def market_Update(request, id):
    post = MarketPost.objects.get(id=id)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.post_time = timezone.now()
        post.thumbnail = request.FILES.get('image')
        post.save()
        return redirect('market:market_view')
    return render(request, 'marketUpdate.html', {'post':post})

def comment(request, id):
    comments = Comment()
    user_info = UserInfo.objects.get(user_email = request.user)
    if request.method == 'POST':
        comments.MarketPost_id = MarketPost.objects.get(id=id)
        comments.writer = user_info.user_nickname
        comments.body = request.POST['comment']
        comments.user_url = user_info.user_image.url
        comments.save()
        

    return redirect('market:market_Detail', id = id)