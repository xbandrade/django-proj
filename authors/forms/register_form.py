from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Username')
        add_placeholder(self.fields['email'], 'email@address.com')
        add_placeholder(self.fields['first_name'], 'Enter your first name')
        add_placeholder(self.fields['last_name'], 'Enter your last name')
        add_placeholder(self.fields['password'], 'Enter your password')
        add_placeholder(self.fields['password2'], 'Enter your password again')

    username = forms.CharField(
        label='Username',
        help_text=('Username must have letters, numbers or symbols. '
                   'The length should be between 4 and 150 characters.'),
        error_messages={
            'required': 'This field is required',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have 150 characters or less',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={
            'required': 'Enter your first name',
        },
        required=True,
        label='First Name',
    )
    last_name = forms.CharField(
        error_messages={
            'required': 'Enter your last name',
        },
        required=True,
        label='Last Name',
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Email is required'
        },
        required=True,
        label='Email',
        help_text='The email must be valid'
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        help_text=(
            'Password must contain at least one uppercase character, '
            'one lowercase character and one number. The length should be'
            'at least 8 characters.'
        ),
        error_messages={
            'required': 'Password must not be empty',
        },
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        validators=[strong_password],
        label='Repeat Password',
        error_messages={
            'required': 'Please repeat your password',
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if 'admin' in data:
            raise ValidationError(
                'Forbidden username',
                code='invalid',
            )
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                'User email is already in use', code='invalid'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            password_error = ValidationError(
                'Passwords must match',
                code='invalid',
            )
            raise ValidationError({
                'password2': [
                    password_error,
                ],
            })
