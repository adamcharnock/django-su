# -*- coding: utf-8 -*-

import warnings
from collections.abc import Callable

from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    SESSION_KEY,
    authenticate,
    login,
)

def su_in(request, user_id):
    '''
    Returns: a User Object or None
    '''
    if not request.user.has_perm("auth.change_user"):
        return None

    userobj = authenticate(request=request, su=True, user_id=user_id)
    if not userobj:
        return None

    exit_users_pk = request.session.get("exit_users_pk", default=[])
    exit_users_pk.append(
        (request.session[SESSION_KEY], request.session[BACKEND_SESSION_KEY])
    )

    maintain_last_login = hasattr(userobj, "last_login")
    if maintain_last_login:
        last_login = userobj.last_login

    try:
        if not custom_login_action(request, userobj):
            login(request, userobj)
        request.session["exit_users_pk"] = exit_users_pk
    finally:
        if maintain_last_login:
            userobj.last_login = last_login
            userobj.save(update_fields=["last_login"])

        return userobj

def su_login_callback(user):
    if hasattr(settings, "SU_LOGIN"):
        warnings.warn(
            "SU_LOGIN is deprecated, use SU_LOGIN_CALLBACK",
            DeprecationWarning,
        )

    func = getattr(settings, "SU_LOGIN_CALLBACK", None)
    if func is not None:
        if not isinstance(func, Callable):
            func = import_string(func)
        return func(user)
    return user.has_perm("auth.change_user")


def custom_login_action(request, user):
    func = getattr(settings, "SU_CUSTOM_LOGIN_ACTION", None)
    if func is None:
        return False

    if not isinstance(func, Callable):
        func = import_string(func)
    func(request, user)

    return True
