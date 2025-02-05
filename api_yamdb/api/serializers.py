import re
from datetime import datetime as dt
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.tokens import RefreshToken

from .configs import CONFIG, USER_CONFIG
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class BaseCategoryGenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'

    def validate_slug(self, value):
        if self.Meta.model.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'поле слага должно быть уникальным')

        if not re.match('^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'поле слага должно соответсвовать указанной структуре')

        if len(value) > CONFIG.get('slug_max_length'):
            raise serializers.ValidationError(
                'длина слага не может быть более 50 символов')

        return value


class CategorySerializer(BaseCategoryGenreSerializer):

    class Meta(BaseCategoryGenreSerializer.Meta):
        model = Category


class GenreSerializer(BaseCategoryGenreSerializer):

    class Meta(BaseCategoryGenreSerializer.Meta):
        model = Genre


class BaseTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(BaseTitleSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()


class TitleWriteSerializer(BaseTitleSerializer):
    description = serializers.CharField(
        allow_blank=True,
        required=False)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)

    def validate_genre(self, value):
        if not value:
            return value
        genres = Genre.objects.all()
        for genre in value:
            if genre not in genres:
                raise serializers.ValidationError(
                    f'жанр {genre} не найден в базе')
        return value

    def validate_category(self, value):
        if value and value not in Category.objects.all():
            raise serializers.ValidationError(
                f'категория {value} не найдена в базе')
        return value

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'нельзя добавить ещё невышедший тайтл')
        return value

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.HiddenField(default=0)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if self.context.get('request').method != 'POST':
            return data
        title_id: int = self.context.get('view').kwargs.get('title_id')
        author: User = self.context.get('request').user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'у вас уже есть отзыв на этот тайтл')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        exclude = ('review',)
        read_only_fields = ('review',)


class MyTokenSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(
            required=True,
            max_length=USER_CONFIG['username_max_length'])
        self.fields['confirmation_code'] = serializers.CharField(required=True)

    def validate(self, attrs):
        self.user = get_object_or_404(User, username=attrs['username'])

        if not default_token_generator.check_token(
                user=self.user,
                token=attrs['confirmation_code']):
            raise serializers.ValidationError('Неверные учетные данные')

        if not self.user.is_active:
            raise serializers.ValidationError('Активной учётной записи с '
                                              'указанными учетными данными '
                                              'не найдено')
        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Необходимо реализовать метод `get_token`'
            'для подклассов `MyTokenSerializer`')


class MyTokenPairSerializer(MyTokenSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(MyTokenPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['token'] = str(refresh.access_token)
        return data


class AuthUserSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Значение 'me' для поля username запрещено, "
                "выберите другое.")
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class UsernameEmailSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USER_CONFIG.get('username_max_length'),
        validators=([RegexValidator(regex=r"^[\w.@+-]+\Z")]))
    email = serializers.EmailField(
        max_length=USER_CONFIG.get('email_max_length'))
