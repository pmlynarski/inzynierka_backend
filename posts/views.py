from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from core.permissions import IsOwnerOrIsMember, IsOwner, IsOwnerOrIsModerator, set_basic_permissions
from core.responses import response406, response200, response404
from groups.models import Group
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer


class PostsViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()

    @action(methods=['GET'], detail=False, url_name="group_post_list", url_path=r'(?P<id>\d+)')
    def group_posts_list(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
        except Group.DoesNotExist:
            return response404('Group')
        self.check_object_permissions(group, request)
        posts = Post.objects.filter(group=group)
        serializer = PostSerializer(posts, many=True)
        paginator = PageNumberPagination()
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(methods=['GET'], detail=False, url_name="user_post_list", url_path='')
    def user_posts_list(self, request, **kwargs):
        posts = Post.objects.filter(group__members_in=request.user) | Post.objects.filter(group__owner=request.user)
        serializer = PostSerializer(posts, many=True)
        paginator = PageNumberPagination()
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(methods=['POST'], detail=False, url_name='create_post', url_path=r'create/(?P<id>\d+)')
    def create_post(self, request, kwargs):
        try:
            group = Group.objects.get(**kwargs)
        except Group.DoesNotExist:
            return response404('Group')
        self.check_object_permissions(request=request, obj=group)
        serializer = PostSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Validation error'})
        serializer.save(group=group)
        return response200({**serializer.data, 'message': 'Successfully created post'})

    @action(methods=['GET'], detail=True, url_name='post_details')
    def get_post(self, request, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get('pk'))
        except Post.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=post.group)
        return response200(PostSerializer(post).data)

    @action(methods=['PUT'], detail=False, url_name='post_delete', url_path=r'update/(?P<id>\d+)')
    def update_post(self, request, **kwargs):
        try:
            post = Post.objects.get(**kwargs)
        except Post.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Validation error'})
        serializer.save()
        return response200({**serializer.data, 'message': 'Successfully updated post'})

    @action(methods=['DELETE'], detail=False, url_name='post_delete', url_path=r'delete/(?P<id>\d+)')
    def delete_post(self, request, **kwargs):
        try:
            post = Post.objects.get(**kwargs)
        except Post.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=post)
        post.delete()
        return response200({'message': 'Successfully deleted post'})

    @action(methods=['POST'], detail=False, url_name='create_comment', url_path=r'create/(?P<id>\d+)/comment')
    def create_comment(self, request, **kwargs):
        try:
            post = Post.objects.get(**kwargs)
        except Post.DoesNotExist:
            return response404('Post')
        serializer = CommentSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Validation error'})
        serializer.save(post=post)
        return response200({**serializer.data, 'message': 'Successfully created comment'})

    @action(methods=['GET'], detail=False, url_name='comment_details', url_path=r'get/(?P<id>\d+)/comment')
    def get_comment(self, request, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs.get('pk'))
        except Comment.DoesNotExist:
            return response404('Comment')
        self.check_object_permissions(request=request, obj=comment.post.group)
        return response200(CommentSerializer(comment).data)

    @action(methods=['PUT'], detail=False, url_name='comment_delete', url_path=r'delete/(?P<id>\d+)/comment')
    def update_comment(self, request, **kwargs):
        try:
            comment = Comment.objects.get(**kwargs)
        except Comment.DoesNotExist:
            return response404('Comment')
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        self.check_object_permissions(request=request, obj=comment)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Validation error'})
        serializer.save()
        return response200({**serializer.data, 'message': 'Successfully updated comment'})

    @action(methods=['DELETE'], detail=False, url_name='post_delete', url_path=r'delete/(?P<id>\d+)')
    def delete_comment(self, request, **kwargs):
        try:
            comment = Comment.objects.get(**kwargs)
        except Comment.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=comment)
        comment.delete()
        return response200({'message': 'Successfully deleted comment'})

    def get_permissions(self):
        action_types = [
            {'class': IsOwnerOrIsMember,
             'values': ['groups_posts_list', 'create_post', 'get_post', 'create_comment', 'get_comment']},
            {'class': IsOwner, 'values': ['groups_posts_list', 'create_post', 'get_post', 'update_comment']},
            {'class': IsOwnerOrIsModerator, 'values': ['delete_post', 'delete_comment']}
        ]
        self.permission_classes = set_basic_permissions(self.action, action_types)
        return [permission() for permission in self.permission_classes]
