"""
Класс вьюсетов для api_yatube
"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Post, Group
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer
from api.permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Метод POST для создания поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Метод для создания queryset комментариев поста."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.all()
        return comments

    def perform_create(self, serializer):
        """Метод POST для создания комментария."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
