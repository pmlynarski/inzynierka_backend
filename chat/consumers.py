# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Message
from chat.serializers import MessageSerializer


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
        headers = {}
        for header in self.scope.get('headers'):
            headers[header[0].decode('UTF-8')] = header[1].decode('UTF-8')
        serializer = MessageSerializer(message, context={'host': headers.get('host')})
        async_to_sync(self.channel_layer.group_send)(
            self.room_id,
            {
                'type': 'chat_message',
                **serializer.data
            }
        )

    def chat_message(self, event):
        sender = to_camel_case({**event.get('sender')})
        output_dict = {**to_camel_case({**event}), 'sender': sender}
        self.send(text_data=json.dumps({
            **output_dict
        }))


def to_camel_case(input_dict: dict) -> dict:
    output_dict = {}
    for key in input_dict.keys():
        if '_' in key:
            splitted = key.split('_')
            for i in range(len(splitted)):
                if i != 0:
                    splitted[i] = splitted[i].capitalize()
            joined = ''.join(splitted)
            output_dict[joined] = input_dict.get(key)
        else:
            output_dict[key] = input_dict.get(key)
    return output_dict
