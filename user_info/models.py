from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models.deletion import CASCADE

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from django.utils import timezone

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserInfo(models.Model):
    user_email = models.CharField(null=True, max_length = 30)
    user_phone = models.CharField(null=True, max_length = 30)
    user_name = models.CharField(null=True, max_length = 20)
    user_account_name = models.CharField(null=True, max_length = 20)
    user_account = models.CharField(null=True, max_length = 30)
    cash = models.CharField(null=True, max_length = 30, blank=True, default='0')
    qua = models.CharField(null=True, max_length = 30, blank=True)

class whodonate(models.Model):
    whogetmoney = models.CharField(null=True, max_length = 30)
    givemoney = models.CharField(null=True, max_length = 30)
    whogivemoney = models.CharField(null=True, max_length = 30)
    what_post = models.ForeignKey("list.Post", on_delete=CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)

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
## abas@naver.com 후원받는사람
## kim@naver.com, tony1234@naver.com 후원하는사람


class Post1(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users1')
    photo = models.ImageField(verbose_name='사진',upload_to='userinfo/',blank=True, null=True)
    post_time = models.DateField(auto_now_add=True)
    body = models.CharField(max_length=500)
    
    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]