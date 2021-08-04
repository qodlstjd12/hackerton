from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from datetime import datetime, timedelta
from user_info.models import CustomUser
from django.utils import timezone

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users')
    # photo = models.ImageField(verbose_name='사진',upload_to='list/',blank=True, null=True)
    post_time = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=500)
    thumbnail = models.ImageField(verbose_name='썸네일', upload_to='thumbnail/')
    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.post_time

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days= 1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days= 7):
            time = datetime.now(tz=timezone.utc).date() - self.post_time.date()
            return str(time.days) + '일 전'
        else:
            return False
class Photo(models.Model):
    post = models.ForeignKey(Post,on_delete=CASCADE, null=True, blank=True)
    image = models.ImageField(verbose_name='사진', upload_to='list/',null=True, blank=True)
#    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(120,80)])
#    thumbnail = models.ImageField(verbose_name='썸네일')
    description = models.TextField()
    def __str__(self):
        return self.description