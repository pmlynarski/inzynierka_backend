from rest_framework import viewsets
from rest_framework.decorators import action

from chat.models import Thread
from chat.serializers import ThreadSerializer, MessageSerializer
from core.responses import response200, response406
from users.models import User


class ChatViewSet(viewsets.GenericViewSet):
    queryset = Thread.objects.all()

    @action(detail=False, methods=['GET', 'POST'], url_name='messages', url_path=r'(?P<id>\d+)')
    def messages(self, request, **kwargs):
        if request.method == 'GET':
            user_2 = User.objects.get(id=kwargs.get('id'))
            try:
                thread = Thread.objects.get_or_create(request.user, user_2)
            except Thread.DoesNotExist:
                return response406({'message': 'Nie możesz czatować sam ze sobą!'})
            serializer = ThreadSerializer(thread, context={'host': request.get_host()})
            return response200({**serializer.data})
        elif request.method == 'POST':
            user_2 = User.objects.get(id=kwargs.get('id'))
            try:
                thread = Thread.objects.get_or_create(request.user, user2=user_2)
            except Thread.DoesNotExist:
                return response406({'message': 'Nie możesz czatować sam ze sobą!'})
            data = {'content': request.data.get('content'), 'thread': thread.id, 'sender': request.user.id}
            serializer = MessageSerializer(data=data)
            if not serializer.is_valid():
                return response406({**serializer.errors, 'message': 'Błędne dane'})
            serializer.save()
            return response200(serializer.data)
