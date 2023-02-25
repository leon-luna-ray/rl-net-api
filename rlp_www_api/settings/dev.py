from .base import *

ALLOWED_HOSTS = ["*"]
# CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:5173', 'http://localhost:5173']
DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
MEDIA_URL = "/media/"
S3_ENABLED = False
SECRET_KEY = "django-insecure-2p*8jk+q!2&jv$3mb*yq(+!#tk35skup&sfe6!950hos-)g_)^"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

try:
    from .local import *
except ImportError:
    pass
