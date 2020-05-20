from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from core.permissions import IsLecturerOrIsAdmin, IsOwnerOrIsModerator, IsMember, set_basic_permissions, \
    IsOwnerOrIsAdmin
from core.responses import response200, response406, response404
from groups.models import Group, PendingMember
from groups.serializers import GroupSerializer, PendingMembersSerializer
from users.models import User


class GroupViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()

    @action(methods=['GET'], detail=False, url_name='search', url_path='search')
    def search_for_groups(self, request):
        try:
            search_phrase = request.GET['phrase']
        except MultiValueDictKeyError:
            return response406({'message': 'Złe dane wejściowe'})
        groups = Group.objects.filter(name__contains=search_phrase)
        groups_data = GroupSerializer(groups, many=True, context={'host': request.get_host}).data
        paginator = PageNumberPagination()
        data = paginator.paginate_queryset(groups_data, request)
        return paginator.get_paginated_response(data)

    @action(methods=['POST'], detail=False, url_name='create_group', url_path='create')
    def create_group(self, request):
        serializer = GroupSerializer(data=request.data, partial=True, context={'host': request.get_host})
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Złe dane wejściowe'})
        serializer.save(owner=request.user)
        return response200(data=serializer.data)

    @action(methods=['GET'], detail=True, url_name='get_group')
    def details(self, request, **kwargs):
        try:
            group = Group.objects.get(id=kwargs.get('pk'))
        except Group.DoesNotExist:
            return response404('Group')
        return response200(
            {**GroupSerializer(group, context={'host': request.get_host}).data, 'message': 'Pomyślnie dodano grupę'})

    @action(methods=['PUT'], detail=False, url_name='update_group', url_path=r'update/(?P<id>\d+)')
    def update_group(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
        except Group.DoesNotExist:
            return response404('Group')
        self.check_object_permissions(request=request, obj=group)
        serializer = GroupSerializer(group, data=request.data, partial=True, context={'host': request.get_host})
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Błąd walidacji'})
        serializer.save()
        return response200(data={**serializer.data, 'message': 'Pomyślnie zaktualizowano grupę'})

    @action(methods=['DELETE'], detail=False, url_name='delete_group', url_path=r'delete/(?P<id>\d+)')
    def delete_group(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
        except Group.DoesNotExist:
            return response404('Group')
        self.check_object_permissions(request=request, obj=group)
        group.delete()
        return response200({'message': 'Pomyślnie usunięto grupę'})

    @action(methods=['POST'], detail=False, url_name='leave_group', url_path=r'leave/(?P<id>\d+)')
    def leave_group(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
        except Group.DoesNotExist:
            return response404('Group')
        self.check_object_permissions(request=request, obj=group)
        group.members.remove(request.user)
        group.save()
        return response200({'message': 'Pomyślnie opuściłeś grupę'})

    @action(methods=['POST'], detail=False, url_name='drop_member', url_path=r'drop/(?P<id>\d+)')
    def drop_member(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
            user = User.objects.get(id=request.data.get('id'))
        except Group.DoesNotExist:
            return response404('Group')
        except User.DoesNotExist:
            return response404('Użytkownik nie znaleziony')
        self.check_object_permissions(request=request, obj=group)
        group.members.remove(user)
        group.save()
        return response200({'message': 'Pomyślnie usunięto użytkownika z grupy'})

    @action(methods=['POST'], detail=False, url_name='join_group', url_path=r'join/(?P<id>\d+)')
    def join_group(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
        except Group.DoesNotExist:
            return response404('Group')
        if request.user in group.members.all() or request.user == group.owner:
            return response406({'message': 'Jesteś już członkiem tej grupy'})
        pending = PendingMember.objects.create(user=request.user, group=group)
        serializer = PendingMembersSerializer(pending, context={'host': request.get_host})
        return response200({**serializer.data, 'message': 'Pomyślnie zapisano się na listę oczekujących'})

    @action(methods=['POST', 'DELETE'], detail=False, url_name='manage_pending_member',
            url_path=r'manage-pending/(?P<id>\d+)')
    def manage_pending_member(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
            pending = PendingMember.objects.get(id=request.data['id'], group=group)
        except Group.DoesNotExist:
            return response404('Group')
        except PendingMember.DoesNotExist:
            return response404('Użytkownik nie znaleziony')
        self.check_object_permissions(request=request, obj=group)
        if request.method == 'POST':
            group.members.add(pending.user)
            message = 'Pomyślnie zaakceptowano użytkownika'
        else:
            message = 'Pomyślnie odrzucono użytkownika'
        pending.delete()
        return response200({'message': message})

    def get_permissions(self):
        action_types = [
            {
                'class': IsOwnerOrIsModerator,
                'values': ['update_group', 'drop_member', 'manage_pending_member']
            },
            {
                'class': IsOwnerOrIsAdmin,
                'values': ['delete_group']
            },
            {
                'class': IsLecturerOrIsAdmin,
                'values': ['create_group']
            },
            {
                'class': IsMember,
                'values': ['leave_group']
            }
        ]
        self.permission_classes = set_basic_permissions(self.action, action_types)
        return [permission() for permission in self.permission_classes]
