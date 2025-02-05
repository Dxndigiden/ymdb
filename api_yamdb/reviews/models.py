from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .mixins import NameSlugMixin
from api.configs import CONFIG

User = get_user_model()


class Category(NameSlugMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Genre(NameSlugMixin):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=CONFIG.get('name_max_length'),
        verbose_name='Название')
    year = models.IntegerField(
        verbose_name='Год выпуска')
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        db_constraint=False)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
        db_constraint=False)


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        db_constraint=False)
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(CONFIG.get('score_max_value')),
            MinValueValidator(CONFIG.get('score_min_value'))])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        db_constraint=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author')]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        db_constraint=False)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время комментария')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        db_constraint=False)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.name
