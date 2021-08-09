# Generated by Django 3.2 on 2021-08-09 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('list', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_nickname', models.CharField(max_length=10, null=True)),
                ('user_email', models.CharField(max_length=30, null=True)),
                ('user_phone', models.CharField(max_length=30, null=True)),
                ('user_image', models.ImageField(default='static/profileimage.jpg', upload_to='userinfo/')),
                ('user_name', models.CharField(max_length=20, null=True)),
                ('user_account_name', models.CharField(max_length=20, null=True)),
                ('user_account', models.CharField(max_length=30, null=True)),
                ('user_totalcash', models.IntegerField(default=0, null=True)),
                ('user_description', models.TextField(default='잘 부탁드립니다!!')),
                ('user_totaldonate', models.IntegerField(default=0, null=True)),
                ('cash', models.IntegerField(default=0, null=True)),
                ('qua', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='whodonate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whogetmoney', models.CharField(max_length=30, null=True)),
                ('givemoney', models.CharField(max_length=30, null=True)),
                ('whogivemoney', models.CharField(max_length=30, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('what_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='list.post')),
            ],
        ),
        migrations.CreateModel(
            name='Post1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='userinfo/', verbose_name='사진')),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('body', models.CharField(max_length=500)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
