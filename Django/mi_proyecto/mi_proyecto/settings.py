"""
Django settings for mi_proyecto project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from django.urls import reverse_lazy
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wqv+r(p67qjygowc4j$ne_s^@l@l#*b)h)&@p*+5*j1s&**01i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "mi-proyecto-73d04.web.app",
    "88c2-83-138-255-48.ngrok-free.app",  # Nueva URL de Ngrok
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Asegúrate de que esté aquí
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "https://mi-proyecto-73d04.web.app",
    "https://88c2-83-138-255-48.ngrok-free.app",  # Nueva URL de Ngrok
]



SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Para guardar las sesiones en la base de datos


ROOT_URLCONF = 'mi_proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Aquí puedes dejar vacío o agregar otras rutas, si es necesario
        ],
        'APP_DIRS': True,  # Esto permite que Django busque plantillas dentro de la carpeta 'templates' en tu app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'mi_proyecto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirecciones después de iniciar/cerrar sesión
LOGIN_REDIRECT_URL = '/post/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login' 


# Ruta donde se guardarán los archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "https://88c2-83-138-255-48.ngrok-free.app",  # Nueva URL de Ngrok
    "https://mi-proyecto-73d04.web.app",
]
CSRF_COOKIE_DOMAIN = "mi-proyecto-73d04.web.app"
CSRF_COOKIE_DOMAIN = None  # Esto permite múltiples orígenes en desarrollo
