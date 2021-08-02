from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

from user_info.models import CustomUser

class Post1(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cs')
    # photo = models.ImageField(verbose_name='사진',upload_to='list/',blank=True, null=True)
    post_time = models.DateField(auto_now_add=True)
    body = models.CharField(max_length=500)
    
    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
