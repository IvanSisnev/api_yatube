from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.response import Response

from posts.models import Post, Group, Comment
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied
        serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, post):
        if self.request.user != post.author:
            raise PermissionDenied
        post.delete()


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

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied
        serializer.save()
        return Response(serializer.data)

    def perform_destroy(self, comment):
        if self.request.user != comment.author:
            raise PermissionDenied
        comment.delete()