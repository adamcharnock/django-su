

def get_user_model():
    try:
        from django.contrib.auth import (
            get_user_model as _get_user_model)

        User = _get_user_model()
    except ImportError:
        from django.contrib.auth.models import User

    return User
