from rest_framework import viewsets

from groups.models import Group
from groups.permissions import IsGroupOwner


class GroupViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()

    def get_permissions(self):
        group_owner_actions = ['delete', 'accept_pending']
        if self.action in group_owner_actions:
            self.permission_classes.append(IsGroupOwner)
        return [permission() for permission in self.permission_classes]
