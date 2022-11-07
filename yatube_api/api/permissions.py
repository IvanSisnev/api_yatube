"""
Классы permissions для приложения api
"""
from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Класс пермишн для сериализаторов, пропускающий только автора объекта.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
