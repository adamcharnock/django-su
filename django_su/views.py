# -*- coding: utf-8 -*-

import warnings

from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate, user_logged_in
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from . import get_user_model
from .forms import UserSuForm
from .utils import su_login_callback, custom_login_action


@csrf_protect
@require_http_methods(['POST'])
@user_passes_test(su_login_callback)
def login_as_user(request, user_id):
    userobj = authenticate(su=True, user_id=user_id)
    if not userobj:
        raise Http404("User not found")

    exit_users_pk = request.session.get("exit_users_pk", default=[])
    exit_users_pk.append(
        (request.session[SESSION_KEY], request.session[BACKEND_SESSION_KEY]))

    maintain_last_login = hasattr(userobj, 'last_login')
    if maintain_last_login:
        last_login = userobj.last_login

    try:
        if not custom_login_action(request, userobj):
            login(request, userobj)
        request.session["exit_users_pk"] = exit_users_pk
    finally:
        if maintain_last_login:
            userobj.last_login = last_login
            userobj.save(update_fields=['last_login'])

    if hasattr(settings, 'SU_REDIRECT_LOGIN'):
        warnings.warn(
            "SU_REDIRECT_LOGIN is deprecated, use SU_LOGIN_REDIRECT_URL",
            DeprecationWarning,
        )

    return HttpResponseRedirect(
        getattr(settings, "SU_LOGIN_REDIRECT_URL", "/"))


@csrf_protect
@require_http_methods(['POST', 'GET'])
@user_passes_test(su_login_callback)
def su_login(request, form_class=UserSuForm, template_name='su/login.html'):
    form = form_class(request.POST or None)
    if form.is_valid():
        return login_as_user(request, form.get_user().pk)

    return render(request, template_name, {
        'form': form,
    })


def su_logout(request):
    exit_users_pk = request.session.get("exit_users_pk", default=[])
    if not exit_users_pk:
        return HttpResponseBadRequest(
            ("This session was not su'ed into. Cannot exit."))

    user_id, backend = exit_users_pk.pop()

    userobj = get_object_or_404(get_user_model(), pk=user_id)
    userobj.backend = backend

    if not custom_login_action(request, userobj):
        login(request, userobj)
    request.session["exit_users_pk"] = exit_users_pk

    if hasattr(settings, 'SU_REDIRECT_EXIT'):
        warnings.warn(
            "SU_REDIRECT_EXIT is deprecated, use SU_LOGOUT_REDIRECT_URL",
            DeprecationWarning,
        )

    return HttpResponseRedirect(
        getattr(settings, "SU_LOGOUT_REDIRECT_URL", "/"))
