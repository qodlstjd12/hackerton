from .models import Post
from .forms import PostForm
from django.shortcuts import redirect, render
from django.utils import timezone
# Create your views here.

def list_view(request):
    post = Post.objects.all()
    return render(request, 'html/newsfeed.html', {'post':post})

def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            print(post.writer)
            post.post_time = timezone.now()
            print(post.post_time)
            post.photo=request.FILES.get('image')
            print(post.photo.url)
            print(post.photo.path)
            post.save()
            return redirect('list:list_view')
    else:
        form = PostForm()
        return render(request, 'html/new.html',{'post':form})
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('list:list_view')