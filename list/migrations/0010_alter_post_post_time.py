# Generated by Django 3.2 on 2021-08-04 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0009_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='등록 시간'),
        ),
    ]
