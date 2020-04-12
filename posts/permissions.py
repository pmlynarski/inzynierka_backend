from rest_framework import permissions


class IsPostOwner(permissions.BasePermission):
    message = 'You must be post owner to do this'

    def has_object_permission(self, request, view, post):
        return request.user == post.owner


class IsPostOwnerOrIsAdmin(permissions.BasePermission):
    message = 'You must be post owner or admin to do this'

    def has_object_permission(self, request, view, post):
        return request.user.is_admin or request.user == post.owner


class IsCommentOwner(permissions.BasePermission):
    message = 'You must be comment owner to do this'

    def has_object_permission(self, request, view, comment):
        return request.user == comment.owner
