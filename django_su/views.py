# -*- coding: utf-8 -*-

import warnings

from django.conf import settings
from django.contrib.auth import (
    get_user_model,
    login,
)
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .forms import UserSuForm
from .utils import custom_login_action, su_login_callback, su_in


User = get_user_model()


@csrf_protect
@require_http_methods(["POST"])
@user_passes_test(su_login_callback)
def login_as_user(request, user_id):
    if not su_in(request, user_id):
        raise Http404("User not found")

    if hasattr(settings, "SU_REDIRECT_LOGIN"):
        warnings.warn(
            "SU_REDIRECT_LOGIN is deprecated, use SU_LOGIN_REDIRECT_URL",
            DeprecationWarning,
        )

    return HttpResponseRedirect(getattr(settings, "SU_LOGIN_REDIRECT_URL", "/"))


@csrf_protect
@require_http_methods(["POST", "GET"])
@user_passes_test(su_login_callback)
def su_login(request, form_class=UserSuForm, template_name="su/login.html"):
    form = form_class(request.POST or None)
    if form.is_valid():
        return login_as_user(request, form.get_user().pk)

    return render(
        request,
        template_name,
        {
            "form": form,
        },
    )


def su_logout(request):
    exit_users_pk = request.session.get("exit_users_pk", default=[])
    if not exit_users_pk:
        return HttpResponseBadRequest(("This session was not su'ed into. Cannot exit."))

    user_id, backend = exit_users_pk.pop()

    userobj = get_object_or_404(User, pk=user_id)
    userobj.backend = backend

    if not custom_login_action(request, userobj):
        login(request, userobj)
    request.session["exit_users_pk"] = exit_users_pk

    if hasattr(settings, "SU_REDIRECT_EXIT"):
        warnings.warn(
            "SU_REDIRECT_EXIT is deprecated, use SU_LOGOUT_REDIRECT_URL",
            DeprecationWarning,
        )

    return HttpResponseRedirect(getattr(settings, "SU_LOGOUT_REDIRECT_URL", "/"))
