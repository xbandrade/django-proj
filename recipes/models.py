from collections import defaultdict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

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
        )


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

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(lambda: [])
        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()
        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    _('Found recipes with the same title')
                )
        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
