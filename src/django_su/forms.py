from django import forms
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class UserSuForm(forms.Form):

    user = forms.ModelChoiceField(label=_('users'),
                  queryset=User.objects.all(),
                  required=True)

    def __init__(self, *args, **kwargs):
        super(UserSuForm, self).__init__(*args, **kwargs)
        self.need_jquery = False
        if 'ajax_select' in settings.INSTALLED_APPS and \
            getattr(settings, 'AJAX_LOOKUP_CHANNELS', None):
            django_su_lookup = settings.AJAX_LOOKUP_CHANNELS.get('django_su', )
            if django_su_lookup:
                from ajax_select.fields import AutoCompleteSelectField
                old_field = self.fields['user']
                self.fields['user'] = AutoCompleteSelectField('django_su',
                                            required=old_field.required,
                                            label=old_field.label)
                self.need_jquery = True

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
