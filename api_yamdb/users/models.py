from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api.configs import USER_CONFIG


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    password = None
    username = models.CharField(
        verbose_name='логин',
        max_length=USER_CONFIG.get('username_max_length'),
        unique=True,
        validators=([RegexValidator(regex=r"^[\w.@+-]+\Z")]))
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        max_length=USER_CONFIG.get('email_max_length'),
        unique=True)
    first_name = models.CharField(
        verbose_name='имя',
        blank=True,
        max_length=USER_CONFIG.get('first_name_max_length'))
    last_name = models.CharField(
        verbose_name='фамилия',
        blank=True,
        max_length=USER_CONFIG.get('last_name_max_length'))
    bio = models.TextField(
        verbose_name='биография',
        blank=True)
    role = models.CharField(
        verbose_name='пользовательская роль',
        max_length=USER_CONFIG.get('role_max_length'),
        blank=True,
        choices=Role.choices,
        default=Role.USER)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username
