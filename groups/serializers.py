from rest_framework import serializers

from groups.models import Group, PendingMember
from users.models import User
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    members = UserSerializer(many=True, read_only=True)
    moderator = UserSerializer(read_only=True, many=False)
    members_count = serializers.SerializerMethodField('get_count')
    pending_count = serializers.SerializerMethodField('get_pending_count')

    class Meta:
        model = Group
        fields = ['id', 'name', 'owner', 'members', 'members_count', 'pending_count', 'image', 'moderator']

    def get_count(self, instance):
        return instance.members.count() + 1

    def get_pending_count(self, instance):
        return PendingMember.objects.filter(group=instance).count()


class FriendsListSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField('get_members')

    class Meta:
        model = Group
        fields = ['members']

    def get_members(self, instance):
        return instance.members.all().union(User.objects.filter(id=instance.owner.id))


class PendingMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = PendingMember
        fields = ['id', 'user', 'group']
