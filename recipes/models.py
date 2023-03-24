import os
import string
from random import SystemRandom

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:category', args=(self.id,))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True,
        ).order_by('-id') \
            .select_related('category', 'author') \
            .prefetch_related('tags')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(
        max_length=165, verbose_name=_('Description')
    )
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    prep_time = models.IntegerField(verbose_name=_('Prep Time'))
    prep_time_unit = models.CharField(
        max_length=65, verbose_name=_('Prep Time Unit')
    )
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(
        max_length=65, verbose_name=_('Servings Unit')
    )
    prep_steps = models.TextField(verbose_name=_('Prep Steps'))
    prep_steps_is_html = models.BooleanField(
        default=False, verbose_name=_('Prep Steps is HTML')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at')
    )
    is_published = models.BooleanField(
        default=False, verbose_name=_('Is published')
    )
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True,
        default='', verbose_name=_('Cover')
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
        verbose_name=_('Category')
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_('Author')
    )
    tags = models.ManyToManyField(
        Tag, blank=True, default='', verbose_name=_('Tags'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=840):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size
        if original_width <= new_width:
            image_pillow.close()
            return
        new_height = round(new_width * original_height / original_width)
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')
        saved = super().save(*args, **kwargs)
        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError as e:
                print(e)
        return saved

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
