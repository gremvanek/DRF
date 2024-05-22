from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь модератором'

    def has_permission(self, request, view):
        return request.user.role == UserRoles.MODERATOR and request.user.is_staff


class IsOwner(BasePermission):
    message = 'Доступ запрещен. Вы не являетесь владельцем'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
