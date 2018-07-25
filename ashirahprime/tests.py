from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.utils import timezone

from allauth.account.models import EmailAddress
from model_mommy import mommy

from . import views


class HomeTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='user1',
            email='user1@ashirahprime.com',
            password='password1',
            first_name = 'firstname1',
            last_name = 'lastname1'
        )

    def test_home(self):
        # logged out
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # logged in
        self.client.login(username='user1', password='password1')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='user1',
            email='user1@ashirahprime.com',
            password='password1',
            first_name = 'firstname1',
            last_name = 'lastname1'
        )

        EmailAddress.objects.create(
            email=self.user.email,
            verified=True,
            primary=True,
            user_id=self.user.pk,
        )

    def test_user_exists(self):
        users = User.objects.all()
        self.assertIn(self.user, users)

    def test_signup(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'user2@ashirahprime.com',
            'email2': 'user2@ashirahprime.com',
            'username': 'user2',
            'password1': 'password2',
            'password2': 'password2',
        }
        response = self.client.post('/accounts/signup/', data)
        self.assertRedirects(response, '/accounts/confirm-email/', 302, 200)

        user = User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.username, data['username'])

    def test_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

        data = {
            'login': self.user.username,
            'password': 'password1',
        }
        response = self.client.post('/accounts/login/', data)
        self.assertRedirects(response, '/', 302, 200)