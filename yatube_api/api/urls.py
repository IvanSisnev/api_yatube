"""
URL configuration for api app.
"""
from rest_framework.routers import SimpleRouter
from django.urls import include, path

from api.views import PostViewSet, GroupViewSet, CommentViewSet

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comment')

urlpatterns = [
    path('api/v1/', include(router.urls))
]
