from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'created_at', 'is_published', 'author'
    list_display_links = 'title', 'created_at'
    search_fields = 'id', 'title', 'description', 'slug', 'prep_steps'
    list_filter = 'category', 'author', 'is_published', 'prep_steps_is_html'
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',),
    }
    autocomplete_fields = 'tags',


admin.site.register(Category, CategoryAdmin)
