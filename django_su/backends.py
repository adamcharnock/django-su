# -*- coding: utf-8 -*-

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class SuBackend(object):
    supports_inactive_user = True

    def authenticate(self, su=False, user_id=None, **kwargs):
        if not su:
            return None

        try:
            user = User._default_manager.get(pk=user_id)  # pylint: disable=W0212
        except (User.DoesNotExist, ValueError):
            return None

        return user

    def get_user(self, user_id):
        try:
            return User._default_manager.get(pk=user_id)  # pylint: disable=W0212
        except User.DoesNotExist:
            return None
