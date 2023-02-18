from collections import defaultdict

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = errors or defaultdict(lambda: [])
        self.ErrorClass = ErrorClass or ValidationError
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_prep_time()
        self.clean_prep_steps()
        cd = self.data
        title = cd.get('title')
        description = cd.get('description')
        if title == description:
            self.errors['description'].append(_('Cannot be same as title'))
        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get('title')
        if len(title) < 5:
            self.errors['title'].append(
                _('Title must have at least 5 characters')
            )
        return title

    def clean_prep_time(self):
        field_name = 'prep_time'
        field_value = self.data.get(field_name)
        if not is_positive_number(field_value):
            self.errors[field_name].append(
                _('Prep time should be positive')
            )
        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)
        if not is_positive_number(field_value):
            self.errors[field_name].append(
                _('Servings should be positive')
            )
        return field_value

    def clean_prep_steps(self):
        field_name = 'prep_steps'
        field_value = self.data.get(field_name)
        if field_value and len(field_value) < 5:
            self.errors[field_name].append(
                _('Prep steps must have at least 5 characters')
            )
        return field_value
