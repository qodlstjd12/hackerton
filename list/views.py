from .models import Post, Photo
from .forms import PostForm
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def list_view(request):
    post = Post.objects.all()
    photo = Photo.objects.all()
    return render(request, 'html/feed.html', {'post':post, 'photo':photo})

@csrf_exempt
def new(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            print(post.writer)
            post.post_time = timezone.now()
            print(post.post_time)
            images = request.FILES.getlist('images')
            post.thumbnail = images[0]
            print(post.thumbnail.url)
            post.save()
            for image in images:
                photo = Photo.objects.create(
                    post=post,
                    image=image,
                    description='photo_test',
                )
        return redirect('list:list_view')
    return render(request, 'html/new.html',{'post':form})
        
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

def feed_Detail(request):
    return render(request, 'html/feedDetail.html')

def helpWrite(request):
    
    return render(request, 'html/helpWrite.html')