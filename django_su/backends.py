try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class SuBackend(object):

    def authenticate(self, su=False, pk=None, **credentials):

        if not su:
            return None

        return User.objects.get(pk=pk)

    def get_user(self, pk):
        return User.objects.get(pk=pk)
