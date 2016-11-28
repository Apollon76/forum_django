from django.db import models
import django.contrib.auth.models


class Post(models.Model):
    author = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.SET_NULL, null=True)
    data = models.CharField(max_length=100000)


class Thread(models.Model):
    name = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post)


class Section(models.Model):
    name = models.CharField(max_length=100)
    threads = models.ManyToManyField(Thread)
