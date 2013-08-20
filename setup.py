import os.path
import sys
from setuptools import setup, find_packages

sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')]
from django_su import __version__

setup(
    name='django-su',
    version=__version__,
    description="Login as any user from the Django admin interface, then switch back when done",
    long_description=open('README.rst').read() if os.path.exists("README.rst") else "",
    author="Adam Charnock",
    author_email="adam@adamcharnock.com",
    url="https://github.com/adamcharnock/django-su",
    license="MIT",

    install_requires=["django"],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.6",
        "Topic :: Security",
        "Framework :: Django",
    ],

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
