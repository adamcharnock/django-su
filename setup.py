#!/usr/bin/env python

import codecs
import os
import sys

from setuptools import find_packages, setup


# When creating the sdist, make sure the django.mo file also exists:
if "sdist" in sys.argv or "develop" in sys.argv:
    os.chdir("django_su")
    try:
        from django.core import management

        management.call_command("compilemessages", stdout=sys.stderr, verbosity=1)
    except ImportError:
        if "sdist" in sys.argv:
            raise
    finally:
        os.chdir("..")


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="django-su",
    version=read("VERSION"),
    license="MIT License",
    install_requires=[
        "django>=2.2",
    ],
    requires=[
        "Django (>=2.2)",
    ],
    description="Login as any user from the Django admin interface, then switch back when done",
    long_description=read("README.rst"),
    author="Adam Charnock",
    author_email="adam@adamcharnock.com",
    maintainer="Basil Shubin",
    maintainer_email="basil.shubin@gmail.com",
    url="http://github.com/adamcharnock/django-su",
    download_url="https://github.com/adamcharnock/django-su/zipball/master",
    packages=find_packages(exclude=("example*", "*.tests*")),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
