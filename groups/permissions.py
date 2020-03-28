from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Tylko administrator może to robić'

    def has_permission(self, request, view):
        return request.user.is_admin


class IsGroupOwner(permissions.BasePermission):
    message = 'Nie jesteś właścicielem grupy'

    def has_object_permission(self, request, view, group):
        return request.user == group.owner
