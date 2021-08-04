from django.db import models
from user_info.models import CustomUser
# Create your models here.

class MarketPost(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    post_time = models.DateField(auto_now_add=True)
    body = models.CharField(max_length=500)
    thumbnail = models.ImageField(verbose_name='썸네일', upload_to='market/')

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]