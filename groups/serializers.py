from rest_framework import serializers

from groups.models import Group, PendingMember
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'owner', 'members']


class PendingMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    group = GroupSerializer(many=False, read_only=True)

    class Meta:
        model = PendingMember
        fields = ['id', 'user', 'group']
