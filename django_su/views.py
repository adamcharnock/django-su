from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext

from django_su.forms import UserSuForm
from django_su.utils import can_su_login, get_static_url

from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY

@user_passes_test(can_su_login)
def login_as_user(request, user_id):
    su_user = authenticate(su=True,pk=user_id)

    if not su_user:
        raise Http404("User not found")

    exit_user_pk = (request.session[SESSION_KEY],request.session[BACKEND_SESSION_KEY])
    exit_users_pk = request.session.get("exit_users_pk", default=[])
    exit_users_pk.append(exit_user_pk)
    login(request, su_user)
    request.session["exit_users_pk"] = exit_users_pk
    return HttpResponseRedirect(getattr(settings, "SU_REDIRECT_LOGIN", "/"))


@user_passes_test(can_su_login)
def su_login(request, user_form=UserSuForm):
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
    staff_user = User.objects.get(pk=exit_users_pk[-1][0])
    staff_user.backend = exit_users_pk[-1][1]
    login(request, staff_user)
    request.session["exit_users_pk"] = exit_users_pk[:-1]
    return HttpResponseRedirect(getattr(settings, "SU_REDIRECT_EXIT", "/"))
