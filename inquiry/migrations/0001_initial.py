# Generated by Django 3.2 on 2021-08-09 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('post_time', models.DateField(auto_now_add=True)),
                ('body', models.CharField(max_length=500)),
            ],
        ),
    ]
