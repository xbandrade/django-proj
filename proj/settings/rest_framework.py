REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': 'rest_framework_simplejwt.authentication.JWTAuthentication',  # noqa
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # noqa
}
