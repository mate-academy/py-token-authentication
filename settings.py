INSTALLED_APPS = [
    # ...
    "rest_framework",
    "rest_framework.authtoken",
    # ...
    "cinema",
    "user",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}
