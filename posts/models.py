from django.db import models

from grouper.settings import MEDIA_ROOT
from groups.models import Group
from users.models import User


class Post(models.Model):
    content = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=MEDIA_ROOT, default=None, null=True)
    file = models.FileField(upload_to=MEDIA_ROOT, default=None, null=True)


class Comment(models.Model):
    content = models.TextField(max_length=250)
    date_commented = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
