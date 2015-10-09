# -*- coding: utf-8 -*-

def is_su(request):
    exit_users_pk = request.session.get("exit_users_pk", default=[])
    return {'DJANGO_SU_IS_SU': len(exit_users_pk) > 0}
