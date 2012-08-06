from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.views import redirect_to_login

import urlparse

from django_su.forms import UserSuForm
from django_su.utils import can_su_login, get_static_url


@login_required
def login_as_user(request, user_id):
    su_user = get_object_or_404(User, pk=user_id)
    if not can_su_login(request.user, su_user):
        # Following is copied from the user_passes_test source
        path = request.build_absolute_uri()
        login_scheme, login_netloc = urlparse.urlparse(settings.LOGIN_URL)[:2]
        current_scheme, current_netloc = urlparse.urlparse(path)[:2]
        if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
            path = request.get_full_path()
        return redirect_to_login(path)
    exit_user_pk = request.user.pk
    su_user.backend = settings.AUTHENTICATION_BACKENDS[0]
    exit_users_pk = request.session.get("exit_users_pk", default=[])
    exit_users_pk.append(exit_user_pk)
    login(request, su_user)
    request.session["exit_users_pk"] = exit_users_pk
    return HttpResponseRedirect(getattr(settings, "SU_REDIRECT_LOGIN", "/"))


@login_required
def su_login(request, user_form=UserSuForm):
    su_user = get_object_or_404(User, pk=user_id)
    if not can_su_login(request.user, su_user):
        return user_passes_test(lambda u: False)()
    data = None
    if request.method == 'POST':
        data = request.POST
    form = user_form(data=data)
    if form.is_valid():
        user = form.get_user()
        return login_as_user(request, user.pk)
    return render_to_response('su/login.html',
                              {'form': form,
                               'STATIC_URL': get_static_url()},
                              context_instance=RequestContext(request))


def su_exit(request):
    exit_users_pk = request.session.get("exit_users_pk", default=[])
    if not exit_users_pk:
        return HttpResponseBadRequest(("This session was not su'ed into."
                                       "Cannot exit."))
    staff_user = User.objects.get(pk=exit_users_pk[-1])
    staff_user.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, staff_user)
    request.session["exit_users_pk"] = exit_users_pk[:-1]
    return HttpResponseRedirect(getattr(settings, "SU_REDIRECT_EXIT", "/"))
