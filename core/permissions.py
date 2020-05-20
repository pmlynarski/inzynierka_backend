from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsLecturerOrIsAdmin(permissions.BasePermission):
    message = 'Musisz być wykładowcą lub administratorem by wykonać tą akcję'

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_lecturer


class IsOwnerOrIsModerator(permissions.BasePermission):
    message = 'Musisz być właścicielem lub moderatorem grupy by wykonać tą akcję'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.moderator or request.user == obj.owner


class IsOwner(permissions.BasePermission):
    message = 'Musisz być właścicielem by wykonać tą akcję'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsMember(permissions.BasePermission):
    message = 'Musisz być członkiem grupy by wykonać tą akcję'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsOwnerOrIsMember(permissions.BasePermission):
    message = 'Musisz być właścicielem grupy lub jej członkiem by wykonać tą akcję'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.members.all()


class IsAdmin(permissions.BasePermission):
    message = 'Musisz być administratorem by wykonać tą akcję'

    def has_permission(self, request, view):
        return request.user.is_admin


class IsOwnerOrIsAdmin(permissions.BasePermission):
    message = 'Musisz być administratorem lub właścicielem by wykonać tą akcję'

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user == obj.owner


class IsPostOwnerOrIsGroupOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user == obj.group.owner or request.user == obj.moderator


class IsCommentOwnerOrIsGroupOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user == obj.post.group.owner or request.user == obj.group.moderator


def set_basic_permissions(action, action_types):
    permissions_to_return = [IsAuthenticated]
    for action_type in action_types:
        if action in action_type['values']:
            permissions_to_return = [*permissions_to_return, action_type['class']]
    return permissions_to_return
