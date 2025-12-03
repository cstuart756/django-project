from .settings import *

# SECURITY
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files (optional)
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Secret key (do NOT hardcode in production)
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-default-for-dev-only')

# Database (example: PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'mydb'),
        'USER': os.environ.get('DB_USER', 'myuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'mypassword'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
