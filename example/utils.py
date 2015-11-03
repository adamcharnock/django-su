# -*- coding: utf-8 -*-

from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
try:
    from django.contrib.auth import HASH_SESSION_KEY
except ImportError:
    HASH_SESSION_KEY = '_auth_user_hash'

from django_su import get_user_model


def su_login_callback(user):
    if user.is_active and user.is_staff:
        return True
    return user.has_perm('auth.change_user')


def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.

    return get_user_model()._meta.pk.to_python(request.session[SESSION_KEY])


def custom_login(request, user):
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                session_auth_hash and
                request.session.get(HASH_SESSION_KEY) != session_auth_hash):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = user.backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user

    try:
        from django.middleware.csrf import rotate_token
        rotate_token(request)
    except ImportError:
        pass
