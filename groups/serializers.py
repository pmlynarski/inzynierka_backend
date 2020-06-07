from rest_framework import serializers

from groups.models import Group, PendingMember
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    members = UserSerializer(many=True, read_only=True)
    moderator = UserSerializer(read_only=True, many=False)
    image = serializers.SerializerMethodField('get_image')
    members_count = serializers.SerializerMethodField('get_count')
    pending_count = serializers.SerializerMethodField('get_pending_count')

    class Meta:
        model = Group
        fields = ['id', 'name', 'owner', 'members', 'members_count', 'pending_count', 'image', 'moderator']

    def get_image(self, instance):
        if instance.image:
            return 'http://' + self.context.get('host') + '/media/' + str(instance.image)
        return None

    def get_count(self, instance):
        return instance.members.count() + 1

    def get_pending_count(self, instance):
        return PendingMember.objects.filter(group=instance).count()


class PendingMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = PendingMember
        fields = ['id', 'user', 'group']
