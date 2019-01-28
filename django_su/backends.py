# -*- coding: utf-8 -*-

from . import get_user_model


class SuBackend(object):
    supports_inactive_user = False

    def authenticate(self, request=None, su=False, user_id=None, **kwargs):
        if not su:
            return None

        user_model = get_user_model()

        try:
            user = user_model._default_manager.get(
                pk=user_id)  # pylint: disable=W0212
        except (user_model.DoesNotExist, ValueError):
            return None

        return user

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model._default_manager.get(
                pk=user_id)  # pylint: disable=W0212
        except user_model.DoesNotExist:
            return None
