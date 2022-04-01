django-su
=========

Login as any user from the Django admin interface, then switch back when done

Authored by `Adam Charnock <http://adamcharnock.com/>`_, and some great
`contributors <https://github.com/adamcharnock/django-su/contributors>`_.

.. image:: https://img.shields.io/pypi/v/django-su.svg
    :target: https://pypi.python.org/pypi/django-su/

.. image:: https://img.shields.io/pypi/dm/django-su.svg
    :target: https://pypi.python.org/pypi/django-su/

.. image:: https://img.shields.io/github/license/adamcharnock/django-su.svg
    :target: https://pypi.python.org/pypi/django-su/

.. image:: https://img.shields.io/travis/adamcharnock/django-su.svg
    :target: https://travis-ci.org/adamcharnock/django-su/

.. image:: https://coveralls.io/repos/adamcharnock/django-su/badge.svg?branch=develop
    :target: https://coveralls.io/r/adamcharnock/django-su?branch=develop

Installation
------------

1. Either checkout ``django_su`` from GitHub, or install using ``pip`` :

   .. code-block:: bash

       pip install django-su

2. Add ``django_su`` to your ``INSTALLED_APPS``. Make sure you put it *before* ``django.contrib.admin`` :

   .. code-block:: python

       INSTALLED_APPS = (
           ...
           'django_su',  # must be before ``django.contrib.admin``
           'django.contrib.admin',
       )

3. Add ``SuBackend`` to ``AUTHENTICATION_BACKENDS`` :

   .. code-block:: python

       AUTHENTICATION_BACKENDS = (
           ...
           'django_su.backends.SuBackend',
       )

4. Update your ``urls.py`` file :

   .. code-block:: python

       urlpatterns = [
           url(r'^su/', include('django_su.urls')),
           ...
       ]

And that should be it!

Please see ``example`` application. This application is used to manually test
the functionalities of this package. This also serves as a good example.

``django-su`` is tested on Django 2.2 or above, lower versions may work, but are considered unsupported.

External dependencies (optional, but recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following apps are optional but will enhance the user experience:

* The 'login su' form will render using `django-form-admin`_
* The user selection widget will render using `django-ajax-selects`_

Note that `django-ajax-selects`_ requires the following settings:

.. code-block:: python

    AJAX_LOOKUP_CHANNELS = {'django_su':  dict(model='auth.user', search_field='username')}


Configuration (optional)
------------------------

There are various optional configuration options you can set in your ``settings.py``

.. code-block:: python

    # URL to redirect after the login.
    # Default: "/"
    SU_LOGIN_REDIRECT_URL = "/"

    # URL to redirect after the logout.
    # Default: "/"
    SU_LOGOUT_REDIRECT_URL = "/"

    # A function specifying the permissions a user requires in order
    # to use the django-su functionality.
    # Default: None
    SU_LOGIN_CALLBACK = "example.utils.su_login_callback"

    # A function to override the django.contrib.auth.login(request, user)
    # view, thereby allowing one to set session data, etc.
    # Default: None
    SU_CUSTOM_LOGIN_ACTION = "example.utils.custom_login"

Usage
-----

Go and view a user in the admin interface and look for a new "Login
as" button in the top right.

Once you have su'ed into a user, you can get exit back into your
original user by navigating to ``/su/`` in your browser.

How to
------

How to Notify superuser when connected with another user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This option warns the superuser when working with another user as
initially logged in. To activate this option perform:

1. Add ``django_su.context_processors.is_su`` to ``TEMPLATE_CONTEXT_PROCESSORS`` :

   .. code-block:: python

       TEMPLATE_CONTEXT_PROCESSORS = (
           ...
           'django_su.context_processors.is_su',
       )

2. In your ``base.html`` include ``su/is_su.html`` snippet :

   .. code-block:: html+django

       {% include "su/is_su.html" %}

How to use django-su with a custom user model (AUTH_USER_MODEL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django-su should function normally with a custom user model. However,
your `ModelAdmin` in your `admin.py` file will need tweaking as follows:

.. code-block:: python

   # Within your admin.py file
   from django.contrib import admin
   from django.contrib.auth.admin import UserAdmin

   from . import models

    @admin.register(models.CustomUser)
    class CustomUserAdmin(UserAdmin):
        # The following two lines are needed:
        change_form_template = "admin/auth/user/change_form.html"
        change_list_template = "admin/auth/user/change_list.html"

This ensures the Django admin will use the correct template customisations for
your custom user model.


Credits
-------

This app was put together by Adam Charnock, but was largely based on ideas, code and comments at:

* http://bitkickers.blogspot.com/2010/06/add-button-to-django-admin-to-login-as.html
* http://copiousfreetime.blogspot.com/2006/12/django-su.html

django-su is packaged using seed_.

.. _django-form-admin: http://pypi.python.org/pypi/django-form-admin
.. _django-ajax-selects: http://pypi.python.org/pypi/django-ajax-selects
.. _seed: https://github.com/adamcharnock/seed/
