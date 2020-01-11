from rest_framework.permissions import BasePermission


class PremiumUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Premium'):
            return True
        return False
