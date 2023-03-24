from rest_framework import serializers

from authors.validators import AuthorRecipeValidator
from recipes.models import Recipe
from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name',]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author', 'category', 'tags',
            'public', 'preparation', 'tag_objects', 'tag_links',
            'prep_time', 'prep_time_unit', 'servings', 'servings_unit',
            'prep_steps', 'cover',
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.prep_time} {recipe.prep_time_unit}'

    def validate(self, attrs):
        if self.instance and not attrs.get('servings'):
            attrs['servings'] = self.instance.servings
        if self.instance and not attrs.get('prep_time'):
            attrs['prep_time'] = self.instance.prep_time
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )
        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
