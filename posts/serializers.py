from rest_framework import serializers

from groups.serializers import GroupSerializer
from posts.models import Post, Comment
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    group = GroupSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'owner', 'group']


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'owner']
