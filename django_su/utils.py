# -*- coding: utf-8 -*-

import warnings
import collections

from django.conf import settings
from django.utils.module_loading import import_string


def su_login_callback(user):
    if hasattr(settings, 'SU_LOGIN'):
        warnings.warn(
            "SU_LOGIN is deprecated, use SU_LOGIN_CALLBACK",
            DeprecationWarning,
        )

    func = getattr(settings, 'SU_LOGIN_CALLBACK', None)
    if func is not None:
        if not isinstance(func, collections.Callable):
            func = import_string(func)
        return func(user)
    return user.has_perm('auth.change_user')


def custom_login_action(request, user):
    func = getattr(settings, 'SU_CUSTOM_LOGIN_ACTION', None)
    if func is None:
        return False

    if not isinstance(func, collections.Callable):
        func = import_string(func)
    func(request, user)

    return True
