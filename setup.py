import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from tz_detect import __version__

setup(
    name='django-su',
    version=__version__,
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    license='MIT License',
    description="Login as any user from the Django admin interface, then switch back when done",
    long_description=README,
    url='http://github.com/adamcharnock/django-su',
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    install_requires=[
        'django>=1.4',
    ],    
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',        
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)
