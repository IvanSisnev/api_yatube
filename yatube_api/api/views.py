from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response

from posts.models import Post, Group, Comment
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_update(post)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return self.perform_update(comment)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(comment)

