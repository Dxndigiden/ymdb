from rest_framework import routers

from django.urls import include, path

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    AuthUser,
    TokenObtainView)
from users.views import UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    'Review',)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    'Comment',)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)


urlpatterns = [
    path('auth/signup/', view=AuthUser, name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain_pair'),
    path('', include(router_v1.urls)),
]
