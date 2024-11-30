from dal import autocomplete
from django.contrib.auth import get_user_model
from django.forms import widgets
from django.test import TestCase, override_settings

from django_su.forms import UserSuDalForm


User = get_user_model()


class TestSuForms(TestCase):
    def setUp(self):
        super(TestSuForms, self).setUp()

        user = User.objects.create(username="user")
        user.set_password("pass")
        user.save()
        self.user = user

    @override_settings(SU_DAL_VIEW_NAME="sampleview")
    def test_dal_form_use_autocomplete_widget(self):
        """Ensure form uses autocomplete widget when SU_DAL_VIEW_NAME is present"""
        form = UserSuDalForm(data={"user": self.user})
        self.assertIsInstance(form.fields["user"].widget, autocomplete.ModelSelect2)

    def test_dal_form_use_default_widget_if_dal_view_not_set(self):
        """Ensure form uses default widget when SU_DAL_VIEW_NAME is not present"""
        form = UserSuDalForm(data={"user": self.user})
        self.assertIsInstance(form.fields["user"].widget, widgets.Select)
