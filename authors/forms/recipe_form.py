from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


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
                    ('Servings', _('Servings')),
                    ('Pieces', _('Pieces')),
                    ('Slices', _('Slices')),
                )
            ),
            'prep_time_unit': forms.Select(
                choices=(
                    ('Minutes', _('Minutes')),
                    ('Seconds', _('Seconds')),
                    ('Hours', _('Hours')),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if title == description:
            self._my_errors['description'].append(_('Cannot be same as title'))
        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            self._my_errors['title'].append(
                _('Title must have at least 5 characters')
            )
        return title

    def clean_prep_time(self):
        field_name = 'prep_time'
        field_value = self.cleaned_data.get(field_name)
        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                _('Prep time should be positive')
            )
        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)
        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                _('Servings should be positive')
            )
        return field_value

    def clean_prep_steps(self):
        field_name = 'prep_steps'
        field_value = self.cleaned_data.get(field_name)
        if len(field_value) < 5:
            self._my_errors[field_name].append(
                _('Prep steps must have at least 5 characters')
            )
        return field_value
