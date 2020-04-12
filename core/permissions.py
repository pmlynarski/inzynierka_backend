from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsLecturerOrIsAdmin(permissions.BasePermission):
    message = 'You must be lecturer or admin to perform this action'

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_lecturer


class IsOwnerOrIsModerator(permissions.BasePermission):
    message = 'You must be moderator to perform this action'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.moderator or request.user == obj.owner


class IsOwner(permissions.BasePermission):
    message = 'You must be group owner to perform this action'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsMember(permissions.BasePermission):
    message = 'You must be group member to perform this action'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members


class IsOwnerOrIsMember(permissions.BasePermission):
    message = 'You must be group owner or member to perform this action'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.members


def set_basic_permissions(action, action_types):
    permissions_to_return = [IsAuthenticated]
    for action_type in action_types:
        if action in action_type['values']:
            permissions_to_return = [*permissions_to_return, action_type['class']]
    return permissions_to_return
