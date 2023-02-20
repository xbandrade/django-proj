from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authors.validators import AuthorRecipeValidator
from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(lambda: [])
        add_attr(self.fields.get('prep_steps'), 'class', 'span-2')
        add_attr(self.fields.get('description'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ('title', 'category', 'prep_time', 'prep_time_unit',
                  'servings', 'servings_unit', 'description', 'prep_steps',
                  'cover')
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    (_('Servings'), _('Servings')),
                    (_('Pieces'), _('Pieces')),
                    (_('Slices'), _('Slices')),
                )
            ),
            'prep_time_unit': forms.Select(
                choices=(
                    (_('Minutes'), _('Minutes')),
                    (_('Seconds'), _('Seconds')),
                    (_('Hours'), _('Hours')),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
