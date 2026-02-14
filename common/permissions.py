from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and not request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class CanEditWithIn15Minutes(BasePermission):
    def has_object_permission(self, request, view, obj):
        time_passed = timezone.now() - obj.created_at
        return time_passed <= timedelta(minutes=20)
    
# class IsModerator