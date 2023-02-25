from .base import *
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))
import os

DEBUG = False

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
# CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")
# CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST").split(",")
# DEFAULT_FILE_STORAGE = "portfolio_cms.settings.storage_backends.MediaStorage"
# STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"

S3_ENABLED = True
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
AWS_QUERY_STRING_AUTH = False
AWS_LOCATION = 'static'
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN


try:
    from .local import *
except ImportError:
    pass
