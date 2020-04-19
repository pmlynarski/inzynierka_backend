from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.permissions import IsAdmin
from core.responses import response404, response406, response200
from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'register':
            permission_classes = [AllowAny]
        if self.action == 'accept_user':
            permission_classes = [*permission_classes, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], url_name='register', url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return response406(serializer.data)
        serializer.save()
        return response200(serializer.data)

    @action(detail=False, methods=['put'], url_name='update', url_path='update')
    def update_profile(self, request):
        serializer = UserSerializer(data=request.data, instance=request.user, partial=True)
        if not serializer.is_valid():
            return response406(serializer.errors)
        serializer.save()
        return response200(serializer.data)

    @action(detail=False, methods=['POST'], url_name='accept_user', url_path='accept')
    def accept_user(self, request):
        try:
            instance = User.objects.get(id=id)
        except User.DoesNotExist:
            return response404('User')
        serializer = UserSerializer(instance=instance, data={'active': True})
        if not serializer.is_valid():
            return response406({'message': 'Złe dane wejściowe'})
        serializer.save()
        return response200({'message': 'Pomyślnie aktywowano użytkownika'})
