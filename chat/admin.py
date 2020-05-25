from django.contrib import admin

# Register your models here.
from chat.models import Thread, Message

admin.site.register(Thread)
admin.site.register(Message)
