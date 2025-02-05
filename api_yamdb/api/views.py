from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin)
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.decorators import api_view

from .filters import TitleFilter
from .mixins import PatchNotPutModelMixin
from .permissions import IsAdminModeratorAuthorReadOnly, IsAdminOrAnon
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    AuthUserSerializer,
    UsernameEmailSerializer,
    MyTokenPairSerializer)
from .utils import auth_send_mail

from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class TitleViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    PatchNotPutModelMixin,
    RetrieveModelMixin
):

    _title = None

    queryset = (
        Title.objects
        .order_by('id')
        .select_related('category')
        .prefetch_related('genre')
        .annotate(
            rating=Avg('reviews__score'),
        )
    )
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrAnon,)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_object(self):
        if not self._title:
            self._title = super().get_object()
        return self._title


class GenreViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    queryset = Genre.objects.order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrAnon,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrAnon,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CommentReviewBase(
    viewsets.GenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    PatchNotPutModelMixin,
    RetrieveModelMixin,
):
    def get_review(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return review


class ReviewViewSet(CommentReviewBase):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorReadOnly,)

    def get_queryset(self):
        queryset = Review.objects.filter(
            title=self.kwargs['title_id']
        ).order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(CommentReviewBase):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorReadOnly,)

    def get_queryset(self):
        review = self.get_review()
        queryset = review.comments.order_by('id')
        return queryset

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


class TokenObtainView(TokenViewBase):
    serializer_class = MyTokenPairSerializer


@api_view(['POST'])
def AuthUser(request):
    request_serializer = UsernameEmailSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)

    email = request_serializer.validated_data.get('email')
    username = request_serializer.validated_data.get('username')
    if User.objects.filter(username=username,
                           email=email).exists():
        exist_user = User.objects.get(username=username)
        code = default_token_generator.make_token(exist_user)
        auth_send_mail(new_user=False, user=exist_user, code=code)
        keys = ['username', 'email']
        response_data = {
            key: request.data.get(key, None) for key in keys}
        return Response(
            data=response_data,
            status=status.HTTP_200_OK)
    create_serializer = AuthUserSerializer(data=request.data)
    create_serializer.is_valid(raise_exception=True)
    create_serializer.save()
    username = create_serializer.validated_data.get('username')
    new_user = User.objects.get(username=username)
    code = default_token_generator.make_token(new_user)
    auth_send_mail(new_user=True, user=new_user, code=code)
    return Response(create_serializer.data, status=status.HTTP_200_OK)
