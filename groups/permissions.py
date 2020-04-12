from rest_framework import permissions


class IsLecturerOrIsAdmin(permissions.BasePermission):
    message = 'You must be lecturer or admin to perform this action'

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_lecturer


class IsOwnerOrModerator(permissions.BasePermission):
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
