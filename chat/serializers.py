from rest_framework import serializers

from chat.models import Thread, Message
from users.serializers import UserSerializer


class ThreadSerializer(serializers.ModelSerializer):
    user1 = serializers.SerializerMethodField('get_user1')
    user2 = serializers.SerializerMethodField('get_user2')
    messages = serializers.SerializerMethodField('get_messages', read_only=True)

    def get_user1(self, instance):
        return UserSerializer(instance.user1, context=self.context).data

    def get_user2(self, instance):
        return UserSerializer(instance.user2, context=self.context).data

    def get_messages(self, instance):
        messages = Message.objects.filter(thread=instance).order_by('date_send')
        if not messages.exists():
            return []
        return MessageSerializer(messages, many=True, context=self.context).data

    class Meta:
        model = Thread
        fields = ['id', 'user1', 'user2', 'messages']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'thread', 'content', 'date_send', 'sender']
