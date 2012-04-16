from distutils.core import setup
from setuptools import find_packages


setup(
    name='django-su',
    version="0.2",
    description="Login as any user from the Django admin interface, then switch back when done",
    author="Adam Charnock",
    author_email="adam@continuous.io",
    url="https://github.com/continuous/django-su",
    license="Apache Software License",

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
