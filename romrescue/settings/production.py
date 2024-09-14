import os

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

try:
    from .local import *  # type: ignore # noqa: F403
except ImportError:
    pass
