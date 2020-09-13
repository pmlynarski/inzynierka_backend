from rest_framework import serializers

from posts.models import Post, Comment
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    group = serializers.SerializerMethodField('get_group')

    class Meta:
        model = Post
        fields = ['id', 'content', 'owner', 'group', 'image', 'file', 'date_posted']

    def get_group(self, instance):
        if instance.group.moderator:
            mod_id = instance.group.moderator.id
        else:
            mod_id = None
        return {'id': instance.group.id, 'name': instance.group.name, 'owner': instance.group.owner.id,
                'moderator': mod_id}


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'owner', 'date_commented']
