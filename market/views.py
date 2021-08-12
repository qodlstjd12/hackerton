from django.contrib.auth.backends import RemoteUserBackend
from user_info.models import CustomUser, UserInfo
from django.core import paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import MarketPost, Comment
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

def market_view(request):
    msg = ""
    if not request.user.is_authenticated:
        msg = 'Not_auth'
    elif not request.user.active:
        msg = "email_auth_error"
    post = MarketPost.objects.all().order_by('-id')
    paginator = Paginator(post, 3)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    return render(request, 'market.html', {'posts':post, 'msg':msg})

from django.shortcuts import get_object_or_404

def market_Detail(request,id):
    post = MarketPost.objects.get(id=id)
    user_info = UserInfo.objects.get(user_email = request.user)
    comments = Comment.objects.filter(post=post)    

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
    if request.method == 'POST':
        comment = Comment.objects.create(
            user = UserInfo.objects.get(user_email=request.user.email),
            post = get_object_or_404(MarketPost, pk = id),
            body = request.POST.get('comment'),
            date = timezone.now(),
        )

    return redirect('market:market_Detail', id)