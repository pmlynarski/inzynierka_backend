from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from core.permissions import set_basic_permissions, IsAdminOrIsPostOwnerOrIsGroupOwnerOrIsGroupModerator, \
    IsAdminOrIsCommentOwnerOrIsPostOwnerOrIsGroupOwnerOrIsGroupModerator, IsPostOwner, \
    IsAdminOrIsGroupOwnerOrIsGroupMember
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
        self.check_object_permissions(obj=group, request=request)
        posts = Post.objects.filter(group=group).order_by('date_posted').reverse()
        serializer = PostSerializer(posts, many=True)
        paginator = PageNumberPagination()
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(methods=['GET'], detail=False, url_name="user_post_list", url_path='')
    def user_posts_list(self, request, **kwargs):
        posts = Post.objects.none().union(Post.objects.filter(group__members=request.user)).union(
            Post.objects.filter(group__owner=request.user)).order_by('date_posted').reverse()
        serializer = PostSerializer(posts, many=True)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(methods=['POST'], detail=False, url_name='create_post', url_path=r'create/(?P<id>\d+)')
    def create_post(self, request, **kwargs):
        try:
            group = Group.objects.get(**kwargs)
        except Group.DoesNotExist:
            return response404('Group')
        self.check_object_permissions(request=request, obj=group)
        serializer = PostSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Błąd walidacji'})
        post = serializer.save(group=group, owner=request.user)
        file = request.FILES.get('file', None)
        image = request.FILES.get('image', None)
        if file:
            post.file = file
            post.save()
        if image:
            post.image = image
            post.save()
        return response200({**serializer.data, 'message': 'Pomyślnie utworzono post'})

    @action(methods=['GET'], detail=False, url_name='post_details', url_path=r'post/(?P<id>\d+)')
    def get_post(self, request, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get('id'))
        except Post.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=post.group)
        return response200(PostSerializer(post).data)

    @action(methods=['GET'], detail=False, url_name='post_comments', url_path=r'comments/(?P<id>\d+)')
    def get_comments(self, request, **kwargs):
        paginator = PageNumberPagination()
        try:
            post = Post.objects.get(id=kwargs.get('id'))
        except Post.DoesNotExist:
            return paginator.get_paginated_response(data=[])
        comments = Comment.objects.filter(post=post).order_by('date_commented').reverse()
        self.check_object_permissions(request=request, obj=post.group)
        serializer = CommentSerializer(comments, many=True)
        paginator.page_size = 10
        data = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(data=data)

    @action(methods=['PUT'], detail=False, url_name='post_update', url_path=r'update/(?P<id>\d+)')
    def update_post(self, request, **kwargs):
        try:
            post = Post.objects.get(**kwargs)
        except Post.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=post)
        file = request.FILES.get('file', None)
        image = request.FILES.get('image', None)
        if file:
            post.file = file
            post.save()
            request.data.pop('post')
        if image:
            post.image = image
            post.save()
            request.data.pop('image')
        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Błąd walidacji'})
        serializer.update(post, serializer.validated_data)
        return response200({**serializer.data, 'message': 'Pomyślnie zaktualizowano posta'})

    @action(methods=['DELETE'], detail=False, url_name='post_delete', url_path=r'delete/(?P<id>\d+)')
    def delete_post(self, request, **kwargs):
        try:
            post = Post.objects.get(**kwargs)
        except Post.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=post)
        post.delete()
        return response200({'message': 'Pomyślnie usunięto posta'})

    @action(methods=['POST'], detail=False, url_name='create_comment', url_path=r'create/comment/(?P<id>\d+)')
    def create_comment(self, request, **kwargs):
        try:
            post = Post.objects.get(**kwargs)
        except Post.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=post.group)
        serializer = CommentSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Błąd walidacji'})
        serializer.save(post=post, owner=request.user)
        return response200({**serializer.data, 'message': 'Pomyślnie utworzono komentarz'})

    @action(methods=['PUT'], detail=False, url_name='comment_update', url_path=r'update/comment/(?P<id>\d+)')
    def update_comment(self, request, **kwargs):
        try:
            comment = Comment.objects.get(**kwargs)
        except Comment.DoesNotExist:
            return response404('Comment')
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        self.check_object_permissions(request=request, obj=comment)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Błąd walidacji'})
        serializer.save()
        return response200({**serializer.data, 'message': 'Pomyślnie zaktualizowano komentarz'})

    @action(methods=['DELETE'], detail=False, url_name='comment_delete', url_path=r'delete/comment/(?P<id>\d+)')
    def delete_comment(self, request, **kwargs):
        try:
            comment = Comment.objects.get(**kwargs)
        except Comment.DoesNotExist:
            return response404('Post')
        self.check_object_permissions(request=request, obj=comment)
        comment.delete()
        return response200({'message': 'Pomyślnie usunięto posta'})

    def get_permissions(self):
        action_types = [
            {
                'class': IsAdminOrIsPostOwnerOrIsGroupOwnerOrIsGroupModerator,
                'values': ['delete_post']
            },
            {
                'class': IsAdminOrIsCommentOwnerOrIsPostOwnerOrIsGroupOwnerOrIsGroupModerator,
                'values': ['delete_comment']
            },
            {
                'class': IsPostOwner,
                'values': ['update_post', 'update_comment']
            },
            {
                'class': IsAdminOrIsGroupOwnerOrIsGroupMember,
                'values': ['group_posts_list', 'create_post', 'get_post', 'get_comments', 'create_comment']
            },
        ]
        self.permission_classes = set_basic_permissions(self.action, action_types)
        return [permission() for permission in self.permission_classes]
