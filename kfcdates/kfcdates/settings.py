"""
Django settings for kfcdates project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')$0ec2a=!%hy4cq-09h7go4*i3j3*mj1e%o7hlvgsyjvs9=j75'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_facebook',
    'core',
    'social.apps.django_app.default',
   
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware'
)

AUTHENTICATION_BACKENDS = (
     'django_facebook.auth_backends.FacebookBackend',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
   
)

ROOT_URLCONF = 'kfcdates.urls'

WSGI_APPLICATION = 'kfcdates.wsgi.application'


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_facebook.context_processors.facebook',
     'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)


TEMPLATE_DIRS = (
    BASE_DIR + '/core/templates/',
)


#AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'

ROOT_URLCONF = 'kfcdates.urls'


#need to config for this project

# PyMongo config
MONGODB_HOST = 'ds047940.mongolab.com'
MONGODB_PORT = 47940
MONGODB_DATABASE = "kfcdates"
MONGODB_USERNAME = "kfcdates"
MONGODB_PASSWORD = "kfcdates"



STATIC_URL = '/static/'

#Facebook
FACEBOOK_APP_ID = '281620288706422'
FACEBOOK_APP_SECRET = 'abfd4b59048317f3e368c048c4eb0e80'

FACEBOOK_DEFAULT_SCOPE = ['email', 'user_likes']






SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect',
)


SOCIAL_AUTH_FACEBOOK_KEY = '749647048440929'
SOCIAL_AUTH_FACEBOOK_SECRET = '66b1e8afe87bd8f056ce66c5124a20d7'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['user_likes', 'email',  ]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}


