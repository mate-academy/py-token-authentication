import django
from django.conf import settings


def pytest_configure() -> None:
    """Ensure Django settings are configured before test collection."""
    if not settings.configured:
        django.setup()
