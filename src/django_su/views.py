from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404


@user_passes_test(lambda u: u.is_staff)
def login_as_user(request, user_id):
    su_user = get_object_or_404(User, pk=user_id)
    exit_user_pk = request.user.pk
    su_user.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, su_user)
    request.session["exit_user_pk"] = exit_user_pk
    return HttpResponseRedirect("/")


def su_exit(request):
    exit_user_pk = request.session.get("exit_user_pk", default=None)
    if not exit_user_pk:
        return HttpResponseBadRequest(("This session was not su'ed into."
                                       "Cannot exit."))
    staff_user = User.objects.get(pk=exit_user_pk)
    staff_user.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, staff_user)
    return HttpResponseRedirect("/")
