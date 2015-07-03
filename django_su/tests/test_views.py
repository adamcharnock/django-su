from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, Client


class LoginAsUserViewTestCase(TestCase):

    def setUp(self):
        super(LoginAsUserViewTestCase, self).setUp()
        from django_su.views import login_as_user
        self.authorized_user = self.user('authorized', is_superuser=True)
        self.unauthorized_user = self.user('unauthorized')
        self.destination_user = self.user('destination')
        self.view = login_as_user
        self.client = Client()

    def user(self, username, **kwargs):
        user = get_user_model().objects.create(username=username, **kwargs)
        user.set_password('pass')
        user.save()
        return user

    def test_login_success(self):
        """Ensure login works for a valid user"""
        self.client.login(username='authorized', password='pass')
        response = self.client.post(
            reverse('login_as_user', args=[self.destination_user.id])
        )
        self.assertEqual(response.status_code, 302)
        # Check the user is logged in in the session
        self.assertIn(auth.SESSION_KEY, self.client.session)
        self.assertEqual(self.client.session[auth.SESSION_KEY], str(self.destination_user.id))
        # Check the 'exit_users_pk' is set so we know which user to change back to
        self.assertIn('exit_users_pk', self.client.session)
        self.assertEqual(
            self.client.session['exit_users_pk'],
            [['1', 'django.contrib.auth.backends.ModelBackend']],
        )

    def test_login_user_id_invalid(self):
        """Ensure login fails with an invalid user id"""
        self.client.login(username='authorized', password='pass')
        response = self.client.post('/su/abc/')
        self.assertEqual(response.status_code, 404)
        # User should still be logged in, but as the original user
        self.assertIn(auth.SESSION_KEY, self.client.session)
        self.assertEqual(self.client.session[auth.SESSION_KEY], str(self.authorized_user.id))
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
        self.assertEqual(self.client.session[auth.SESSION_KEY], str(self.unauthorized_user.id))
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
        self.assertEqual(response['Location'], 'http://testserver/foo/bar')

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
