from rest_framework import serializers

from chat.models import Thread, Message
from users.serializers import UserSerializer


class ThreadSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(many=False, read_only=True)
    user2 = UserSerializer(many=False, read_only=True)
    last_message = serializers.SerializerMethodField('get_message', read_only=True)

    def get_message(self, instance):
        messages = Message.objects.filter(thread=instance).order_by('date_send')
        if not messages:
            return None
        return MessageSerializer(messages[0]).data

    class Meta:
        model = Thread
        fields = ['id', 'user1', 'user2', 'last_message']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'content', 'date_send', 'sender']
