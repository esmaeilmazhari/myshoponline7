"""
Django settings for myshop project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
# برای رندر بهتر است این مقدار از متغیرهای محیطی خوانده شود، اما فعلا True بماند تا مشکل تصاویر حل شود.
DEBUG = True 

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # Cloudinary apps (باید قبل از staticfiles باشد)
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    
    # Store App
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # WhiteNoise برای مدیریت فایل‌های استاتیک
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart_count', # شمارنده سبد خرید
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'

# Database
# استفاده از SQLite هم برای لوکال و هم برای رندر
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# تنظیمات جدید فایل‌های استاتیک و مدیا (جایگزین تنظیمات منسوخ شده)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Cloudinary Settings برای ذخیره دائمی تصاویر
# هشدار امنیتی: در محیط واقعی این مقادیر را در Environment Variables رندر قرار دهید
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'whkl2ilw',
    'API_KEY': '617893514988949',
    'API_SECRET': 'fRcxIkVb-xo1mAx0-ack3jbWEzY'
}

MEDIA_URL = '/media/'

# Cart Session ID
CART_SESSION_ID = 'cart'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'