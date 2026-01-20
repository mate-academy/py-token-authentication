# settings.py

INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'rest_framework.authtoken',  # Required for Token Auth
    'user',
    'cinema',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'cinema.permissions.IsAdminOrIfAuthenticatedReadOnly',
    ),
}
