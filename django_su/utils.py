# -*- coding: utf-8 -*-

import warnings
import collections

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def importpath(path, error_text=None):
    """
    Import value by specified ``path``.
    Value can represent module, class, object, attribute or method.
    If ``error_text`` is not None and import will
    raise ImproperlyConfigured with user friendly text.
    """
    result = None
    attrs = []
    parts = path.split('.')
    exception = None
    while parts:
        try:
            result = __import__('.'.join(parts), {}, {}, [''])
        except ImportError as e:
            if exception is None:
                exception = e
            attrs = parts[-1:] + attrs
            parts = parts[:-1]
        else:
            break
    for attr in attrs:
        try:
            result = getattr(result, attr)
        except (AttributeError, ValueError) as e:
            if error_text is not None:
                raise ImproperlyConfigured('Error: %s can import "%s"' % (
                    error_text, path))
            else:
                raise exception
    return result


def su_login_callback(user):
    if hasattr(settings, 'SU_LOGIN'):
        warnings.warn(
            "SU_LOGIN is deprecated, use SU_LOGIN_CALLBACK",
            DeprecationWarning,
        )

    func = getattr(settings, 'SU_LOGIN_CALLBACK', None)
    if func is not None:
        if not isinstance(func, collections.Callable):
            func = importpath(func)
        return func(user)
    return user.has_perm('auth.change_user')


def custom_login_action(request, user):
    func = getattr(settings, 'SU_CUSTOM_LOGIN_ACTION', None)
    if func is None:
        return False

    if not isinstance(func, collections.Callable):
        func = importpath(func)
    func(request, user)

    return True
