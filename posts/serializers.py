from rest_framework import serializers

from groups.serializers import GroupSerializer
from posts.models import Post, Comment
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')
    group = serializers.SerializerMethodField('get_group')
    image = serializers.SerializerMethodField('get_image')
    file = serializers.SerializerMethodField('get_file')

    class Meta:
        model = Post
        fields = ['id', 'content', 'owner', 'group', 'image', 'file']

    def get_image(self, instance):
        if instance.image:
            return 'http://' + self.context.get('host') + instance.image
        return None

    def get_file(self, instance):
        if instance.file:
            return 'http://' + self.context.get('host') + instance.file
        return None

    def get_group(self, instance):
        return GroupSerializer(instance.group, context=self.context).data

    def get_owner(self, instance):
        return UserSerializer(instance.owner, context=self.context)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'owner']

    def get_owner(self, instance):
        return UserSerializer(instance.owner, context=self.context).data
