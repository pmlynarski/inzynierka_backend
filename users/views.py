from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.permissions import IsAdmin
from core.responses import response404, response406, response200
from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        admin_actions = ['accept_user', 'unaccepted_users']
        self.permission_classes = [IsAuthenticated]
        if self.action == 'register':
            self.permission_classes = [AllowAny]
        if self.action in admin_actions:
            self.permission_classes = [*self.permission_classes, IsAdmin]
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['post'], url_name='register', url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data, context={'host': request.get_host()})
        if not serializer.is_valid():
            return response406(serializer.errors)
        serializer.save()
        return response200(serializer.data)

    @action(detail=False, methods=['put'], url_name='update', url_path='update')
    def update_profile(self, request):
        user = User.objects.get(id=request.data.get('id'))
        serializer = UserSerializer(data=request.data, instance=request.user, partial=True,
                                    context={'host': request.get_host()})
        if not serializer.is_valid():
            return response406(serializer.errors)
        serializer.update(user, serializer.validated_data)
        return response200(serializer.data)

    @action(detail=False, methods=['POST'], url_name='accept_user', url_path=r'accept/(?P<id>\d+)')
    def accept_user(self, request, **kwargs):
        try:
            instance = User.objects.get(id=kwargs.get('id'))
        except User.DoesNotExist:
            return response404('User')
        serializer = UserSerializer(instance=instance, data={'active': True}, partial=True,
                                    context={'host': request.get_host()})
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Złe dane wejściowe'})
        serializer.save()
        return response200({'message': 'Pomyślnie aktywowano użytkownika'})

    @action(detail=False, methods=['GET'], url_name='unaccepted_users', url_path='unaccepted_users')
    def unaccepted_users(self, request):
        users = User.objects.filter(active=False)
        if len(users) == 0:
            return response404('Users')
        serializer = UserSerializer(users, many=True, context={'host': request.get_host()})
        return response200(serializer.data)

    @action(detail=False, methods=['GET'], url_name='current_user', url_path='current_user')
    def get_current_user(self, request):
        return response200(UserSerializer(request.user, context={'host': request.get_host()}).data)

    @action(detail=False, methods=['GET'], url_name='get', url_path=r'get/(?P<id>\d+)')
    def get_by_id(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))
        except User.DoesNotExist:
            return response404('Użytkownik')
        serializer = UserSerializer(user, context={'host': request.get_host()})
        return response200(serializer.data)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return response200({
            **UserSerializer(user, context={'host': request.get_host()}).data,
            'token': token.key
        })
