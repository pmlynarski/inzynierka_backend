from django.db import models

from users.models import User


def upload_location(instance, filename):
    return "group%s/%s" % (instance.id, filename)


class Group(models.Model):
    name = models.CharField(max_length=127, null=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='moderator', null=True)
    members = models.ManyToManyField(User, related_name='members')
    image = models.ImageField(upload_to=upload_location, default='default-group.jpg')


class PendingMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
