# Generated by Django 3.2 on 2021-08-06 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0018_userinfo_user_totalcash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='cash',
            field=models.IntegerField(default=0, null=True),
        ),
    ]