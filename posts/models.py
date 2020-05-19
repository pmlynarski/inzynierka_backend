from django.db import models

from grouper.settings import MEDIA_ROOT
from groups.models import Group
from users.models import User


class Post(models.Model):
    content = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=MEDIA_ROOT, default=None)
    file = models.ImageField(upload_to=MEDIA_ROOT, default=None)


class Comment(models.Model):
    content = models.TextField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
