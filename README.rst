django-su
=========

Login as any user from the Django admin interface, then switch back when done

Authored by `Adam Charnock <http://https://adamcharnock.com/>`_, and some great `contributors <https://github.com/adamcharnock/django-su/contributors>`_.

.. image:: https://pypip.in/version/django-su/badge.svg
    :target: https://pypi.python.org/pypi/django-su/

.. image:: https://pypip.in/download/django-su/badge.svg
    :target: https://pypi.python.org/pypi/django-su/

.. image:: https://pypip.in/license/django-su/badge.svg
    :target: https://pypi.python.org/pypi/django-su/

Installation
------------

1. Either checkout ``django_su`` from GitHub, or install using pip:

.. code-block:: bash

    pip install django-su

2. Add ``django_su`` to your ``INSTALLED_APPS``. Make sure you put it *before* ``django.contrib.admin``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_su',  # must be before ``django.contrib.admin``
        'django.contrib.admin',
    )

3. Add ``SuBackend`` to ``AUTHENTICATION_BACKENDS``:

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        ...
        'django_su.backends.SuBackend',
    )

4. Update your ``urls.py`` file:

.. code-block:: python

    urlpatterns = patterns('',
        url(r'^su/', include('django_su.urls')),
        ...
    )

And that should be it!

Please see ``example`` application. This application is used to manually test the functionalities of this package. This also serves as a good example.

You need only Django 1.4 or above to run that. It might run on older versions but that is not tested.

External dependencies (optional, but recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you install these two eggs the enhance user experience:

* The 'login su' form will render using `django admin forms`_
* The user selection widget will render using `django ajax selects`_

Note that `django ajax selects`_ requires the following settings:

.. code-block:: python
    AJAX_LOOKUP_CHANNELS = {'django_su':  dict(model='auth.user', search_field='username')}

   
Configuration (optional)
------------------------

There are various optional configuration options you can set in your settings.py::

``SU_REDIRECT_LOGIN``: URL to redirect after the login. By default is "/"
``SU_REDIRECT_EXIT``: URL to redirect after the logout. By default is "/"
``SU_LOGIN``: A function to specify the perms that the user must have can use django_su
``SU_CUSTOM_LOGIN_ACTION``: A function to override the django.contrib.auth.login(request, user) function so you can set session data, etc.

Usage
-----

Go and view a user in the admin interface and look for a new "Login as" button in the top right.

Once you have su'ed into a user, you can get exit back into your original user by navigating to ``/su/`` in your browser.

Credits
-------

This app was put together by Adam Charnock, but was largely based on ideas, code and comments at:

* http://bitkickers.blogspot.com/2010/06/add-button-to-django-admin-to-login-as.html
* http://copiousfreetime.blogspot.com/2006/12/django-su.html

django-su is packaged using seed_.

.. _django admin forms: http://pypi.python.org/pypi/django-form-admin
.. _django ajax selects: http://pypi.python.org/pypi/django-ajax-selects
.. _seed: https://github.com/adamcharnock/seed/
