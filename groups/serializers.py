from rest_framework import serializers

from groups.models import Group, PendingMember
from users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner')
    members = serializers.SerializerMethodField('get_members')
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Group
        fields = ['id', 'name', 'owner', 'members', 'image']

    def get_owner(self, instance):
        return UserSerializer(instance.owner, context=self.context).data

    def get_members(self, instance):
        return UserSerializer(instance.members, context=self.context, many=True).data

    def get_image(self, instance):
        if instance.image:
            print(instance.image)
            return 'http://' + self.context.get('host') + '/' + str(instance.image)
        return None


class PendingMembersSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = PendingMember
        fields = ['id', 'user', 'group']

    def get_user(self, instance):
        return UserSerializer(instance.user, context=self.context).data
