import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

TEMPLATE_DIRS = [
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_templates'),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
    },
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    
    'django_su',
    'django.contrib.admin',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

MIDDLEWARE = MIDDLEWARE_CLASSES

ROOT_URLCONF = 'test_urls'

SITE_ID = 1

STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_su.backends.SuBackend',
]
