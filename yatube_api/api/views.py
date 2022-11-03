"""
Класс вьюсетов для api_yatube
"""
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from posts.models import Post, Group, Comment
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Метод POST для создания поста."""
        serializer.save(author=self.request.user)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """Методы PUT, PATCH для изменения поста."""
        if self.request.user != serializer.instance.author:
            raise PermissionDenied
        serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """Метод DELETE для удаления поста."""
        if self.request.user != instance.author:
            raise PermissionDenied
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Метод для создания queryset комментариев поста."""
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        """Метод POST для создания комментария."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Методы PUT, PATCH для изменения комментария."""
        if self.request.user != serializer.instance.author:
            raise PermissionDenied
        serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """Метод DELETE для удаления комментария."""
        if self.request.user != instance.author:
            raise PermissionDenied
        instance.delete()
