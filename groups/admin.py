# Register your models here.
from django.contrib import admin

from groups.models import Group, PendingMember

admin.site.register(Group)
admin.site.register(PendingMember)