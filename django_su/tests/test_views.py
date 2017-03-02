from django.conf import settings
from django.contrib import auth
from django.test import TestCase, Client
from django.contrib.sessions.backends import cached_db
from django.utils.datetime_safe import datetime

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

try:
    from django.contrib.auth import get_user_model, user_logged_in

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class SuViewsBaseTestCase(TestCase):

    def setUp(self):
        super(SuViewsBaseTestCase, self).setUp()
        from django_su.views import login_as_user
        self.authorized_user = self.user('authorized', is_superuser=True)
        self.unauthorized_user = self.user('unauthorized')
        self.destination_user = self.user('destination')
        self.view = login_as_user
        self.client = self.make_client()
        # Causes errors with validation.
        # TODO: Investigate
        if 'ajax_select' in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS.remove('ajax_select')

    def user(self, username, **kwargs):
        user = User.objects.create(username=username, **kwargs)
        user.set_password('pass')
        user.save()
        return user

    def make_client(self):
        client = Client()
        s = cached_db.SessionStore()
        s.save()
        client.cookies[settings.SESSION_COOKIE_NAME] = s.session_key
        return client


class LoginAsUserViewTestCase(SuViewsBaseTestCase):

    def test_login_success(self):
        """Ensure login works for a valid user"""
        self.client.login(username='authorized', password='pass')
        response = self.client.post(
            reverse('login_as_user', args=[self.destination_user.id])
        )
        self.assertEqual(response.status_code, 302)
        # Check the user is logged in in the session
        self.assertIn(auth.SESSION_KEY, self.client.session)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.destination_user.id))
        # Check the 'exit_users_pk' is set so we know which user to change back to
        self.assertIn('exit_users_pk', self.client.session)
        pk, backend = self.client.session['exit_users_pk'][0]
        self.assertEqual(str(pk), str(self.authorized_user.pk))
        self.assertEqual(backend, 'django.contrib.auth.backends.ModelBackend')

    def test_login_user_id_invalid(self):
        """Ensure login fails with an invalid user id"""
        self.client.login(username='authorized', password='pass')
        response = self.client.post('/su/abc/')
        self.assertEqual(response.status_code, 404)
        # User should still be logged in, but as the original user
        self.assertIn(auth.SESSION_KEY, self.client.session)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.authorized_user.id))
        # Exit user should never get set
        self.assertNotIn('exit_users_pk', self.client.session)

    def test_login_without_permission(self):
        """Ensure login fails when the current user lacks permission"""
        self.client.login(username='unauthorized', password='pass')
        with self.settings(SU_LOGIN_CALLBACK=None):
            response = self.client.post(
                reverse('login_as_user', args=[self.destination_user.id])
            )
        self.assertEqual(response.status_code, 302)
        # User should still be logged in, but as the original user
        self.assertIn(auth.SESSION_KEY, self.client.session)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.unauthorized_user.id))
        # Exit user should never get set
        self.assertNotIn('exit_users_pk', self.client.session)

    def test_custom_su_login_url(self):
        """Ensure user is sent to login url following successful login"""
        self.client.login(username='authorized', password='pass')
        with self.settings(SU_LOGIN_REDIRECT_URL='/foo/bar'):
            response = self.client.post(
                reverse('login_as_user', args=[self.destination_user.id])
            )
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/foo/bar' in response['Location'])

    def test_custom_login_action(self):
        """Ensure custom login action is called"""
        self.client.login(username='authorized', password='pass')

        flag = { 'called': False }
        def custom_action(request, user):
            flag['called'] = True

        with self.settings(SU_CUSTOM_LOGIN_ACTION=custom_action):
            response = self.client.post(
                reverse('login_as_user', args=[self.destination_user.id])
            )
        self.assertTrue(flag['called'])

    def test_last_login_not_changed(self):
        self.destination_user.last_login = datetime(2000, 1, 1)
        self.destination_user.save()
        self.client.login(username='authorized', password='pass')
        response = self.client.post(
            reverse('login_as_user', args=[self.destination_user.id])
        )
        self.destination_user = User.objects.get(pk=self.destination_user.pk)
        self.assertEqual(self.destination_user.last_login, datetime(2000, 1, 1))
        # Check the update_last_login function has been reconnected to the user_logged_in signal
        connections = [str(ref[1]) for ref in auth.user_logged_in.receivers if 'update_last_login' in str(ref[1])]
        self.assertTrue(connections)


    def test_login_signal_reconnected_following_error(self):
        self.client.login(username='authorized', password='pass')
        def error_action(request, user):
            raise Exception()
        with self.settings(SU_CUSTOM_LOGIN_ACTION=error_action):
            try:
                response = self.client.post(
                    reverse('login_as_user', args=[self.destination_user.id])
                )
            except:
                pass
        # Check the update_last_login function has been reconnected to the user_logged_in signal
        connections = [str(ref[1]) for ref in auth.user_logged_in.receivers if 'update_last_login' in str(ref[1])]
        self.assertTrue(connections)


class LoginViewTestCase(SuViewsBaseTestCase):

    def test_get_authorised(self):
        """Load the login page as an authorised user"""
        self.client.login(username='authorized', password='pass')
        response = self.client.get(reverse('su_login'))
        self.assertEqual(response.status_code, 200)

    def test_get_unauthorised(self):
        """Load the login page as an authorised user"""
        self.client.login(username='unauthorized', password='pass')
        response = self.client.get(reverse('su_login'))
        self.assertEqual(response.status_code, 302)

    def test_post_unauthorised(self):
        """Post to the login page as an authorised user"""
        self.client.login(username='unauthorized', password='pass')
        response = self.client.post(reverse('su_login'))
        self.assertEqual(response.status_code, 302)

    def test_post_valid(self):
        """Ensure posting valid data logs the user in"""
        self.client.login(username='authorized', password='pass')
        response = self.client.post(reverse('su_login'), data=dict(
            user=self.destination_user.id
        ))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.destination_user.id))

    def test_post_non_existent(self):
        """Ensure posting a non-existent user does not log the user in"""
        self.client.login(username='authorized', password='pass')
        response = self.client.post(reverse('su_login'), data=dict(
            user='999'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.authorized_user.id))

    def test_post_invalid(self):
        """Ensure posting invalid data redisplays the form and does not log the user in"""
        self.client.login(username='authorized', password='pass')
        response = self.client.post(reverse('su_login'), data=dict(
            user='abc'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.authorized_user.id))


class LogoutViewTestCase(SuViewsBaseTestCase):

    def test_valid_get(self):
        """Ensure user can logout via get"""
        s = self.client.session
        s['exit_users_pk'] = [
            ['1', 'django.contrib.auth.backends.ModelBackend'],
        ]
        s.save()
        response = self.client.get(reverse('su_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(auth.SESSION_KEY, self.client.session)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.authorized_user.id))

    def test_valid_post(self):
        """Ensure user can logout via post"""
        s = self.client.session
        s['exit_users_pk'] = [
            ['1', 'django.contrib.auth.backends.ModelBackend'],
        ]
        s.save()
        response = self.client.post(reverse('su_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(auth.SESSION_KEY, self.client.session)
        self.assertEqual(str(self.client.session[auth.SESSION_KEY]), str(self.authorized_user.id))

    def test_no_exit_pk(self):
        """Ensure logout fails if no exit pk present in session"""
        response = self.client.get(reverse('su_logout'))
        self.assertEqual(response.status_code, 400)

    def test_non_existant_exit_pk(self):
        """Ensure logout fails if no exit pk present in session"""
        s = self.client.session
        s['exit_users_pk'] = [
            ['999', 'django.contrib.auth.backends.ModelBackend'],
        ]
        s.save()
        response = self.client.get(reverse('su_logout'))
        self.assertEqual(response.status_code, 404)

    def test_redirect_url(self):
        """Ensure logout redirect url setting respected"""
        s = self.client.session
        s['exit_users_pk'] = [
            ['1', 'django.contrib.auth.backends.ModelBackend'],
        ]
        s.save()
        with self.settings(SU_LOGOUT_REDIRECT_URL='/foo/bar'):
            response = self.client.get(reverse('su_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/foo/bar' in response['Location'])
