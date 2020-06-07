from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsAdmin(permissions.BasePermission):
    message = 'Musisz być administratorem'

    def has_permission(self, request, view):
        return request.user.is_admin


# Groups

class IsAdminOrIsLecturer(permissions.BasePermission):
    message = 'Musisz być administratorem lub wykładowcą dla tej akcji'

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_lecturer


class IsAdminOrIsGroupOwnerOrIsGroupMember(permissions.BasePermission):
    message = 'Musisz być członkiem grupy lub administratorem dla tej akcji'

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user == obj.owner or request.user in obj.members.all()


class IsAdminOrIsGroupOwner(permissions.BasePermission):
    message = 'Musisz być administratorem lub właścicielem grupy'

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user == obj.owner


class IsGroupOwner(permissions.BasePermission):
    message = 'Musisz być właścicielem grupy'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsGroupMember(permissions.BasePermission):
    message = 'Musisz być członkiem grupy'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsAdminOrIsGroupOwnerOrIsGroupModerator(permissions.BasePermission):
    message = 'Musisz być administratorem, właścicielem grupy, lub jej moderatorem'

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user == obj.owner or request.user == obj.moderator


# Posts

class IsAdminOrIsPostOwnerOrIsGroupOwnerOrIsGroupModerator(permissions.BasePermission):
    message = 'Nie masz ku temu uprawnień'

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.owner == request.user or \
               obj.group.owner == request.user or obj.group.moderator == request.user


class IsAdminOrIsCommentOwnerOrIsPostOwnerOrIsGroupOwnerOrIsGroupModerator(permissions.BasePermission):
    message = 'Nie masz ku temu uprawnień'

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.owner == request.user or obj.post.owner == request.user or \
               obj.post.group.owner == request.user or obj.post.group.moderator == request.user


class IsPostOwner(permissions.BasePermission):
    message = 'Musisz być właścicielem posta'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


def set_basic_permissions(action, action_types):
    permissions_to_return = [IsAuthenticated]
    for action_type in action_types:
        if action in action_type['values']:
            permissions_to_return = [*permissions_to_return, action_type['class']]
    return permissions_to_return
