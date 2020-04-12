from rest_framework import viewsets
from rest_framework.decorators import action

from core.responses import response406, response200, response404
from posts.models import Post
from posts.serializers import PostSerializer


class PostsViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()

    @action(methods=['POST'], detail=False, url_name='create_post', url_path='create')
    def create_post(self, request):
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return response406({**serializer.errors, 'message': 'Validation error'})
        return response200({**serializer.data, 'message': 'Successfully created post'})

    @action(methods=['GET'], detail=True, url_name='post_details')
    def get_post(self, request, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get('pk'))
        except Post.DoesNotExist:
            return response404('Post')
        return response200(PostSerializer(post).data)

    @action(methods=['PUT'], detail=False, url_name='post_delete', url_path=r'update/(?P<id>\d+)')
    def update_post(self, request, **kwargs):
        try:
            post = Post.objects.get(**kwargs)
        except Post.DoesNotExist:
            return response404('Post')
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
        post.delete()
        return response200({'message': 'Successfully deleted post'})
