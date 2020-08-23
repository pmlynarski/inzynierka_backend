from rest_framework import serializers

from chat.models import Thread, Message
from users.serializers import UserSerializer


class ThreadSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(many=False, read_only=True)
    user2 = UserSerializer(many=False, read_only=True)
    messages = serializers.SerializerMethodField('get_messages', read_only=True)

    def get_messages(self, instance):
        messages = Message.objects.filter(thread=instance).order_by('date_send')[:10]
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
