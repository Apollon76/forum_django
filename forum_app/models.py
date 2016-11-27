from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    registration_date = models.DateTimeField()
    registration_date.null = True
    is_admin = models.BooleanField(default=False)
    email = models.CharField(null=False, max_length=30)

    def __str__(self):
        return self.nickname


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.CharField(max_length=100000)


class Thread(models.Model):
    name = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post)


class Section(models.Model):
    name = models.CharField(max_length=100)
    threads = models.ManyToManyField(Thread)
