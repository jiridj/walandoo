from rest_framework.permissions import BasePermission

class IsSelf(BasePermission):
    """
    Custom permission to only allow users to access their own customer record.
    Assumes the Customer model has a OneToOneField to the User model.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
