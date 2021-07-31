from .models import Post, Photo
from .forms import PostForm
from django.shortcuts import redirect, render
from django.utils import timezone
# Create your views here.

def list_view(request):
    post = Post.objects.all()
    photo = Photo.objects.all()
    return render(request, 'html/newsfeed.html', {'post':post, 'photo':photo})

def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            print(post.writer)
            post.post_time = timezone.now()
            print(post.post_time)
            post.save()
            images = request.FILES.getlist('images')
            for image in images:
                photo = Photo.objects.create(
                    post=post,
                    image=image,
                    description='photo_test'
                )
                print(photo.image.url)

            return redirect('list:list_view')
    else:
        form = PostForm()
        return render(request, 'html/new.html',{'post':form})
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('list:list_view')

    #         if form.is_valid():
    #         post = form.save(commit=False)
    #         post.writer = request.user
    #         print(post.writer)
    #         post.post_time = timezone.now()
    #         print(post.post_time)
    #         post.photo = request.FILES.getlist('images')
    #         print(post.photo.url)
    #         print(post.photo.path)
    #         post.save()
    #         return redirect('list:list_view')
