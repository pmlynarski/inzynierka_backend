from rest_framework import serializers

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
            return 'http://' + self.context.get('host') + str(instance.image)
        return None

    def get_file(self, instance):
        if instance.file:
            return 'http://' + self.context.get('host') + str(instance.file)
        return None

    def get_group(self, instance):
        return {'id': instance.group.id, 'name': instance.group.name}

    def get_owner(self, instance):
        return UserSerializer(instance.owner, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'owner']

    def get_owner(self, instance):
        return UserSerializer(instance.owner, context=self.context).data
