from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE

DEBUG = True

SECRET_KEY = "django-insecure-wj1k2jz@-jv6)6z+jlb_%*_z&37h)^jli$r1&rcd#w(uk46@nl"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += [
    "debug_toolbar",
    "django_browser_reload",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]
INTERNAL_IPS = [
    "127.0.0.1",
]

try:
    from .local import *  # type: ignore # noqa: F403
except ImportError:
    pass
