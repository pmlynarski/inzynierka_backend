from django.db import models

from groups.models import Group
from users.models import User


def upload_location(instance, filename):
    return "post%s/%s" % (instance.id, filename)


class Post(models.Model):
    content = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_location, default=None, null=True, blank=True)
    file = models.FileField(upload_to=upload_location, default=None, null=True, blank=True)


class Comment(models.Model):
    content = models.TextField(max_length=250)
    date_commented = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
