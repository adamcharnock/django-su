.. image:: https://badge.fury.io/py/django-su.png
    :target: https://badge.fury.io/py/django-su

.. image:: https://pypip.in/d/django-su/badge.png
    :target: https://pypi.python.org/pypi/django-su

Installation
============

Step 1: Settings
----------------

Add ``django_su`` to ``INSTALLED_APPS``. Make sure you put it *before* ``django.contrib.admin``.

Step 2: urls.py
---------------

Add this to your root ``urls.py`` file::

    url(r"^su/", include("django_su.urls")),

And that should be it!

Step 3: Install other eggs (optional, but recommended)
------------------------------------------------------

If you install these two eggs the enhance user experience:

 * The 'login su' form will render using `django admin forms`_
 * The user selection widget will render using `django ajax selects`_

Note that `django ajax selects`_ requires the following settings::

    AJAX_LOOKUP_CHANNELS = {'django_su':  dict(model='auth.user', search_field='username')}

Step 4: Customize django_su (optional)
--------------------------------------

In your settings you can configure:

 * ``SU_REDIRECT_LOGIN``: URL to redirect after the login. By default is "/"
 * ``SU_REDIRECT_EXIT``: URL to redirect after the logout. By default is "/"
 * ``SU_LOGIN``: A function to specify the perms that the user must have can use django_su

Usage
-----

Go and view a user in the admin interface and look for a new 'Login as' button in the top right.

Once you have su'ed into a user, you can get exit back into your original user by navigating to ``/su/`` in your browser.

Credits
=======

This app was put together by Adam Charnock, but was largely based on ideas, code and comments at:

* http://bitkickers.blogspot.com/2010/06/add-button-to-django-admin-to-login-as.html
* http://copiousfreetime.blogspot.com/2006/12/django-su.html

django-su is packaged using seed_.

.. _django admin forms: http://pypi.python.org/pypi/django-form-admin
.. _django ajax selects: http://pypi.python.org/pypi/django-ajax-selects
.. _seed: https://github.com/adamcharnock/seed/