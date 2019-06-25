"""
Django settings for applications project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import sys
import os

sys.path.append('/home/pikoto/domains/pikoto.net.pl/Apps/applications')
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&8_e21g6@u(mo6ab#s@gu3#+9*d0!u1^gnii9kr@=!ra+n$w*y'


# SECURITY CAPTCHA WARNING: keep the secret key used in production secret!
RECAPTCHA_PUBLIC_KEY = '6LesrxETAAAAAOX2MHxtylsElLcns0K2JcSeQD4n'
RECAPTCHA_PRIVATE_KEY = '6LesrxETAAAAACssOVmsaP31sov0fgLYc6Ayf_uw'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['instructor.pikoto.net.pl']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'applications',
    'questsions',
    'conf',
    'recaptchawidget',
    'publications'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'applications.urls'

WSGI_APPLICATION = 'applications.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Sessions
SESSION_COOKIE_AGE = 3600#21600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

### Add
#

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    '/domains/pikoto.net.pl/Apps/applications',
)

# Templates files (html)
TEMPLATE_DIRS = (
      os.path.join(BASE_DIR, 'template'),
)
