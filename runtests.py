#!/usr/bin/env python

import sys
from os import path

import django
from django.conf import settings, global_settings
from django.core.management import execute_from_command_line


if not settings.configured:
    BASE_DIR = path.dirname(path.realpath(__file__))

    settings.configure(
        DEBUG = False,
        TEMPLATE_DEBUG = True,
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        TEMPLATE_DIRS = (
            path.join(BASE_DIR, 'test_templates'),
        ),
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [
                    path.join(BASE_DIR, 'test_templates'),
                ],
                'APP_DIRS': True,
            },
        ],
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.sites',
            'django.contrib.sessions',
            'django.contrib.staticfiles',
            'django.contrib.contenttypes',

            'django_su',
            'django.contrib.admin',
        ),
        MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner' if django.VERSION < (1,6) else 'django.test.runner.DiscoverRunner',
        SITE_ID = 1,
        ROOT_URLCONF = 'django_su.tests.test_urls',
        STATIC_URL = '/static/',
        AUTHENTICATION_BACKENDS = (
            "django.contrib.auth.backends.ModelBackend",
            "django_su.backends.SuBackend",
        ),
    )

def runtests():
    argv = sys.argv[:1] + ['test', 'django_su'] + sys.argv[1:]
    execute_from_command_line(argv)

if __name__ == '__main__':
    runtests()
