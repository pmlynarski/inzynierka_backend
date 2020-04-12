from django.db import models

from grouper.settings import MEDIA_ROOT
from users.models import User


class Group(models.Model):
    name = models.CharField(max_length=127, null=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='moderator', null=True)
    members = models.ManyToManyField(User, related_name='members')
    photo = models.ImageField(upload_to=MEDIA_ROOT)


class PendingMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
