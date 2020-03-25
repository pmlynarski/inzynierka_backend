# Create your models here.
from django.db import models

from groups.models import Group
from users.models import User


class Post(models.Model):
    content = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
