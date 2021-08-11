from django.db import models
from user_info.models import CustomUser, UserInfo
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.

class MarketPost(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    post_time = models.DateTimeField(auto_now_add=True, verbose_name="등록 시간")
    body = models.CharField(max_length=500)
    thumbnail = models.ImageField(verbose_name='썸네일', upload_to='market/', null=True)

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

class Comment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    post = models.ForeignKey(MarketPost, on_delete=models.CASCADE, related_name="posts")
    body = models.CharField(max_length=30, blank=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name="registe time")

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days= 1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days= 7):
            time = datetime.now(tz=timezone.utc).date() - self.date.date()
            return str(time.days) + '일 전'
        else:
            return False