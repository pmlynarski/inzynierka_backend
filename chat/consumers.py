# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_id = None
        self.room_id = None

    def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_id = 'chat_%s' % self.thread_id

        async_to_sync(self.channel_layer.group_add)(self.room_id, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_id, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        raw_data = [arg for arg in
                    json.loads(text_data).replace('{', '').replace('}', '').replace(':', '').replace(',', '').split(
                        "\"")
                    if
                    arg != '']
        data_dict = {}
        for i in range(len(raw_data)):
            if i % 2 == 0 and i + 1 <= len(raw_data):
                data_dict = {**data_dict, raw_data[i]: raw_data[i + 1]}
        message = Message(thread_id=self.scope.get('url_route').get('kwargs').get('thread_id'),
                          sender_id=data_dict.get('senderId'), content=data_dict.get('message'))
        message.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_id,
            {
                'type': 'chat_message',
                **data_dict
            }
        )

    def chat_message(self, event):
        message = event.get('message')
        sender_id = event.get('senderId')
        self.send(text_data=json.dumps({
            'message': message,
            'senderId': sender_id
        }))
