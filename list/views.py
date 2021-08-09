from datetime import timedelta
from django.contrib import messages
from django.http.response import HttpResponse
from .models import Post, Photo
from .forms import PostForm
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from user_info.models import CustomUser, UserInfo, whodonate
from django.core.paginator import Paginator
# Create your views here.

def list_view(request):
    post = Post.objects.all().order_by('-id')
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    return render(request, 'html/feed.html', {'posts':post})

@csrf_exempt
def helpWrite(request):
    if not request.user.is_authenticated:
        msg = "Not_auth"
        return render(request, 'html/helpWrite.html', {'msg' : msg})        
    
    userinfo = UserInfo.objects.get(user_email=request.user.email)
    if userinfo.qua != "yes":
        msg = "Not_yes"
        return render(request, 'html/helpWrite.html', {'msg' : msg})

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

#id1 = 주는사람
#id2 = 받는사람
#id3 = 당시 포스트id
@csrf_exempt
def donate(request, id1, id2, id3):
    if request.method == 'POST':
        donator = CustomUser.objects.get(id=id1)
        receiver = CustomUser.objects.get(id=id2)
        cash = int(request.POST.get('cash'))

        donator_info = UserInfo.objects.get(user_email=donator.email)
        receiver_info = UserInfo.objects.get(user_email=receiver.email)

        if cash > int(donator_info.cash):
            return HttpResponse("돈 더 충전하고 오세요")

        relation = whodonate.objects.create(
            whogetmoney= receiver.email,
            givemoney= str(cash),
            whogivemoney= donator.email,
            what_post = Post.objects.get(id=id3),
            date = timezone.now()
        )
        donator_info.user_totaldonate += cash
        print(receiver_info.cash)
        print("Before : " + str(donator_info.cash))
        print("Before : " + str(receiver_info.cash))
        donator_info.cash = int(donator_info.cash) - cash
        receiver_info.cash = str(int(receiver_info.cash) + cash)
        print("After : " + str(donator_info.cash))
        print("After : " + str(receiver_info.cash))

        donator_info.save()
        receiver_info.save()
    return redirect('list:list_view')