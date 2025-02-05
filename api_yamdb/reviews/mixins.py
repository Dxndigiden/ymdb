from django.db import models

from api.configs import CONFIG


class NameSlugMixin(models.Model):
    name = models.CharField(
        max_length=CONFIG.get('name_max_length'),
        verbose_name='Наименование',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=CONFIG.get('slug_max_length'),
    )

    def __str__(self) -> str:
        return self.slug
