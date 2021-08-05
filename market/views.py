from django.core import paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import MarketPost
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

def market_view(request):
    post = MarketPost.objects.all().order_by('-id')
    paginator = Paginator(post, 3)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    return render(request, 'market.html', {'posts':post})

def market_Detail(request,id):
    post = MarketPost.objects.get(id=id)
    return render(request, 'marketDetail.html', {'post':post})

@csrf_exempt
def market_Write(request):
    if request.method == 'POST':
        post = MarketPost()
        post.title = request.POST.get('title')
        post.writer= request.user
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