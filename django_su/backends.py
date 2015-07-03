# -*- coding: utf-8 -*-

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class SuBackend(object):

    def authenticate(self, su=False, pk=None, **credentials):
        if not su:
            return None

        try:
            User._meta.pk.get_prep_value(pk)
        except ValueError:
            return None

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

        return user

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
