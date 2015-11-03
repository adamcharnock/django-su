# -*- coding: utf-8 -*-


def is_su(request):
    return {
        'IS_SU': len(request.session.get("exit_users_pk", default=[]))
    }
