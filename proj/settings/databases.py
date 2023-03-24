import os

import dj_database_url
from django.conf import settings
from dotenv import load_dotenv

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

load_dotenv()

if settings.DEBUG:
    DATABASES = {
        os.environ.get('DATABASE_ALIAS'): {
            'ENGINE': os.environ.get('DATABASE_ENGINE'),
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': os.environ.get('DATABASE_HOST'),
            'PORT': os.environ.get('DATABASE_PORT'),
        }
    }
else:
    DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=True)}  # noqa
