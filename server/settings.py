from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m$m@qgi+4xdaf!j6&=dpfd+kka%up5m)_r2bwxs3!aib-yuer0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["13.49.223.25","16.171.64.245","localhost","127.0.0.1","codeutsava.nitrr.ac.in","tcpmentorship.nitrr.ac.in"]
CORS_ALLOWED_ORIGINS = ["http://13.49.223.25","https://16.171.64.245","http://localhost:5173","http://localhost:3000","https://codeutsava.nitrr.ac.in","http://codeutsava.nitrr.ac.in","https://tcpmentorship.netlify.app","https://tcpmentorship.nitrr.ac.in"]
CSRF_TRUSTED_ORIGINS = ["http://13.49.223.25","https://16.171.64.245","http://localhost:5173","http://localhost:3000","https://codeutsava.nitrr.ac.in","http://codeutsava.nitrr.ac.in", "https://tcpmentorship.netlify.app","https://tcpmentorship.nitrr.ac.in"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'content-type',
    'x-csrftoken',
    'authorization',
]

MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR,'./')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Events.apps.EventsConfig',
    'Speakers.apps.SpeakersConfig',
    'ProblemStatements.apps.ProblemstatementsConfig',
    'Team.apps.TeamConfig',
    'clients.apps.ClientsConfig',
    'Counter.apps.CounterConfig',
    'Glimpses.apps.GlimpsesConfig',
    'ShortlistedTeams.apps.ShortlistedteamsConfig',
    'Sponsors.apps.SponsorsConfig',
    'Winners.apps.WinnersConfig',
    'Questions.apps.QuestionsConfig',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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
            ],
        },
    },
] 

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Short-lived access tokens
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,  # Automatically blacklist old refresh tokens
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
STATIC_ROOT = './static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
