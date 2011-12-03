from django import forms
from django.conf import settings

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserSuForm(forms.Form):

    user = forms.ModelChoiceField(label=_('users'),
                  queryset=User.objects.all(),
                  required=True)

    def __init__(self, *args, **kwargs):
        super(UserSuForm, self).__init__(*args, **kwargs)

    def get_user(self):
        return self.cleaned_data.get('user', None)

    def __unicode__(self):
        if 'formadmin' in settings.INSTALLED_APPS:
            try:
                from formadmin.forms import as_django_admin
                return as_django_admin(self)
            except ImportError:
                pass
        return super(UserSuForm, self).__unicode__()
