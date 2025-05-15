# TODO:  Напишите свой вариант

from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from posts.models import Post, Follow, Group
from .serializers import (
    PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение на изменение только для автора."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class BaseModelViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет с общей логикой."""
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(BaseModelViewSet):
    """Вьюсет для работы с постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'author__username']
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        queryset = self.filter_queryset(self.get_queryset())
        if limit is not None or offset is not None:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from rest_framework.exceptions import NotAuthenticated
            raise NotAuthenticated(
                'Authentication credentials were not provided.'
            )
        return super().create(request, *args, **kwargs)


class CommentViewSet(BaseModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    pagination_class = None
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from rest_framework.exceptions import NotAuthenticated
            raise NotAuthenticated(
                'Authentication credentials were not provided.'
            )
        return super().create(request, *args, **kwargs)


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с подписками."""
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    pagination_class = None

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        user = self.request.user
        following = serializer.validated_data['following']
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError('Вы уже подписаны на этого пользователя.')
        serializer.save(user=user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
