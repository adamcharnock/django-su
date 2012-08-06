from django.conf import settings

import inspect


def import_function(name, package=None):
    path = name.split('.')
    module_path = '.'.join(path[:-1])
    try:
        from django.utils.importlib import import_module
        module = import_module(module_path, package)
    except ImportError:  # compatible with old version of Django
        module = __import__(module_path, {}, {}, path[-1])
    return getattr(module, path[-1])


def can_su_login(user, su_user=None):
    """
    Returns True iff user can change into su_user, or - if su_user is
    None - iff the user can change users at all (for template usage).
    """
    su_login = getattr(settings, 'SU_LOGIN', None)
    if su_login:
        func = import_function(su_login)
        # Pass the function just one argument if that's all
        # it takes, to maintain backward compatibility
        if len(inspect.getargspec(func)[0]) == 1:
            return func(user)
        else:
            return func(user, su_user)
    return user.has_perm('auth.change_user')


def get_static_url():
    static_url = getattr(settings, 'STATIC_URL', None)
    if static_url:
        return static_url
    else:  # To old django versions
        return '%sajax_select/' % getattr(settings, 'MEDIA_URL', None)
