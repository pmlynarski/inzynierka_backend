from rest_framework import serializers

from groups.models import Group, PendingMember
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=False)
    members = UserSerializer(many=True, read_only=False)

    class Meta:
        model = Group
        fields = ['id', 'content', 'owner', 'members']


class PendingMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=False)
    group = GroupSerializer(many=False, read_only=False)

    class Meta:
        model = PendingMember
        fields = ['id', 'user', 'group']
