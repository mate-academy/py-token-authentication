# settings.py

INSTALLED_APPS = [
    # ... suas apps existentes
    'rest_framework',
    'rest_framework.authtoken', # Adicionar para autenticação por token
    # ... suas apps de cinema e user
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Pode ser um bom padrão inicial
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication', # Adicionar Token Authentication
    )
}
