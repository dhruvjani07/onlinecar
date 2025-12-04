from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY - Generated secure key
SECRET_KEY = 'om=!r)ws9mnzcs=+yxqzu9jca*jh6fus)an6rht9o6f#23)zu@'

DEBUG = True

ALLOWED_HOSTS = ['*']

# -------------------------------
# Applications
# -------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',

    # Project Apps
    'vehicles',
    'accounts',
]

# -------------------------------
# Middleware
# -------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webcar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'webcar.context_processors.google_maps_key',
            ],
        },
    },
]

WSGI_APPLICATION = 'webcar.wsgi.application'

# -------------------------------
# Database (AWS RDS PostgreSQL)
# Sensitive: DB_PASSWORD from environment
# -------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'webcaruser',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'dhruvjani07'),
        'HOST': 'webcar-db.clwm06yagu1l.eu-west-1.rds.amazonaws.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# -------------------------------
# Password Validation
# -------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# Localization
# -------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------
# Static Files
# -------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# -------------------------------
# MEDIA — AWS S3
# Sensitive: AWS credentials from environment
# -------------------------------

USE_S3_FOR_MEDIA = True

if USE_S3_FOR_MEDIA:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = 'webcarmedia'
    AWS_S3_REGION_NAME = 'eu-west-1'

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/"
    MEDIA_ROOT = ""
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------
# Crispy Forms
# -------------------------------

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# -------------------------------
# Auth Redirects
# -------------------------------

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'

# -------------------------------
# Google Maps
# -------------------------------

GOOGLE_MAPS_API_KEY = 'AIzaSyAdeAVx_1FG92yL1yoP9LWN8QKyaUI60wE'

# -------------------------------
# Default Primary Key
# -------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'