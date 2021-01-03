from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from chat.models import Thread, Message
from chat.serializers import ThreadSerializer, MessageSerializer
from core.responses import response200, response406, response404
from users.models import User


class ChatViewSet(viewsets.GenericViewSet):
    queryset = Thread.objects.all()

    @action(detail=False, methods=['GET', 'POST'], url_name='messages', url_path=r'(?P<id>\d+)')
    def messages(self, request, **kwargs):
        user_2 = User.objects.get(id=kwargs.get('id'))
        try:
            thread = Thread.objects.get_or_create(request.user, user_2)
        except Thread.DoesNotExist:
            return response406({'message': 'Nie możesz czatować sam ze sobą!'})
        serializer = ThreadSerializer(thread)
        return response200({**serializer.data})

    @action(detail=False, methods=['GET'], url_name='threads', url_path='threads_list')
    def threads_list(self, request, **kwargs):
        user_id = request.user.id
        threads = Thread.objects.filter(user1_id=user_id).union(Thread.objects.filter(user2_id=user_id))
        serializer = ThreadSerializer(threads, many=True)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(detail=False, methods=['GET'], url_name='messages-list', url_path='messages')
    def messages_list(self, request, *args):
        thread_id = request.query_params.get('threadId')
        messages = Message.objects.filter(thread_id=thread_id).order_by('-date_send')
        serializer = MessageSerializer(messages, many=True)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)
