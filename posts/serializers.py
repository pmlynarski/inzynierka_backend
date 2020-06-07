from rest_framework import serializers

from posts.models import Post, Comment
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    group = serializers.SerializerMethodField('get_group')
    image = serializers.SerializerMethodField('get_image')
    file = serializers.SerializerMethodField('get_file')

    class Meta:
        model = Post
        fields = ['id', 'content', 'owner', 'group', 'image', 'file', 'date_posted']

    def get_image(self, instance):
        if instance.image:
            return 'http://' + self.context.get('host') + '/media/' + str(instance.image)
        return None

    def get_file(self, instance):
        if instance.file:
            return 'http://' + self.context.get('host') + '/media/' + str(instance.file)
        return None

    def get_group(self, instance):
        return {'id': instance.group.id, 'name': instance.group.name, 'owner': instance.group.owner.id,
                'moderator': instance.group.moderator.id}


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'owner', 'date_commented']
