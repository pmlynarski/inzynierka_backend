from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.permissions import IsAdmin
from core.responses import response404, response406, response200
from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        admin_actions = ['manage_user', 'users_list', 'set_role']
        self.permission_classes = [IsAuthenticated]
        if self.action == 'register':
            self.permission_classes = [AllowAny]
        if self.action in admin_actions:
            self.permission_classes = [*self.permission_classes, IsAdmin]
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['post'], url_name='register', url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return response406(serializer.errors)
        serializer.save()
        return response200(serializer.data)

    @action(detail=False, methods=['put'], url_name='update', url_path='update')
    def update_profile(self, request):
        user = User.objects.get(id=request.data.get('id'))
        if 'image' in request.data:
            user.image = request.FILES.get('image')
            user.save()
            request.data.pop('image')
        serializer = UserSerializer(data=request.data, instance=request.user, partial=True)
        if not serializer.is_valid():
            return response406(serializer.errors)
        serializer.update(user, serializer.validated_data)
        return response200(UserSerializer(user).data)

    @action(detail=False, methods=['PUT'], url_name='manage_user', url_path=r'manage_user')
    def manage_user(self, request):
        try:
            instance = User.objects.get(id=request.data.get('user_id'))
        except User.DoesNotExist:
            return response404('User')
        if request.user.id == instance.id:
            return response406({'message': 'Nie możesz zablokować sam siebie'})
        future_activity = False
        if not instance.is_active:
            future_activity = True
        instance.active = future_activity
        instance.save()
        return response200({'message': 'Pomyślnie aktywowano użytkownika'})

    @action(detail=False, methods=['GET'], url_name='users_list', url_path='users_list')
    def users_list(self, request):
        sort = request.query_params.get('sort', default='active')
        phrase = request.query_params.get('filter', default=None)
        users = User.objects.all().order_by('{}'.format(sort))
        if phrase:
            users = users.filter(
                Q(email__icontains=phrase) | Q(first_name__icontains=phrase) | Q(last_name__icontains=phrase))
        serializer = UserSerializer(users, many=True)
        paginator = PageNumberPagination()
        paginator.page_size = 30
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(detail=False, methods=['GET'], url_name='current_user', url_path='current_user')
    def get_current_user(self, request):
        return response200(UserSerializer(request.user).data)

    @action(detail=False, methods=['GET'], url_name='get', url_path=r'get/(?P<id>\d+)')
    def get_by_id(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))
        except User.DoesNotExist:
            return response404('Użytkownik')
        serializer = UserSerializer(user)
        return response200(serializer.data)

    @action(detail=False, methods=['PUT'], url_name="set_role", url_path='set_role')
    def set_role(self, request):
        try:
            user = User.objects.get(id=request.data.get('user_id'))
        except User.DoesNotExist:
            return response404('Użytkownik')
        role = request.data.get('role', 0)
        if role == 0:
            user.admin = False
            user.lecturer = False
        elif role == 1:
            user.admin = False
            user.lecturer = True
        elif role == 2:
            user.admin = True
            user.lecturer = False
        user.save()
        return response200({'message': 'Zaktualizowano użytkownika'})


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return response200({
            **UserSerializer(user).data,
            'token': token.key
        })
