from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    FollowViewSet,
    GroupViewSet,
)

router = DefaultRouter()
# Основные вьюсеты
router.register(r'posts', PostViewSet)
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'groups', GroupViewSet, basename='groups')
# Роут для комментариев через DRF-роутер (nested-путь)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='post-comments'
)

urlpatterns = [
    # все endpoint из router на v1/
    path('v1/', include(router.urls)),
    # JWT endpoints
    path('v1/', include('djoser.urls.jwt')),
]
