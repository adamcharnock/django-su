from django.contrib.auth import login

def su_login_callback(user):
    if user.is_active and user.is_staff:
        return True
    return user.has_perm('auth.change_user')

def custom_login(request, user):
    request.session['orson'] = 'welles'
    login(request, user)
