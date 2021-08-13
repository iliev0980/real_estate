from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from copy import deepcopy


def create_user(**params):
    payload = {
        'first_name': 'test first',
        'last_name': 'test second',
        'username': 'testuser',
        'email': 'test@gmail.com',
        'password': 'test123',
    }
    return get_user_model().objects.create_user(**payload)


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        create_user()


    def test_get_register_page(self):
        res = self.client.get(reverse('register'))
        self.assertTemplateUsed(res, 'accounts/register.html')

    def test_creating_user_success_returns_message_and_redirects(self):
        payload = {
            'first_name': 'first name',
            'last_name': 'second name',
            'username': 'testcreateuser',
            'email': 'testuser@gmail.com',
            'password': 'test123',
            'password2': 'test123',
        }
        res = self.client.post(reverse('register'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'You are now registered and can log in')
        self.assertRedirects(res, reverse('login'))

    def test_passwords_doesnt_match_returns_message_and_redirects(self):
        payload = {
            'first_name': 'test first',
            'last_name': 'test second',
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'test123',
            'password2': 'test943',
        }

        res = self.client.post(reverse('register'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'Passwords do not match!')
        self.assertRedirects(res, reverse('register'))

    def test_username_already_exists_returns_message_and_redirects(self):
        payload = {
            'first_name': 'test first',
            'last_name': 'test second',
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'test123',
            'password2': 'test123',
        }

        res = self.client.post(reverse('register'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'That username is taken')
        self.assertRedirects(res, reverse('register'))

    def test_email_already_exists_returns_message_and_redirects(self):
        payload = {
            'first_name': 'test first',
            'last_name': 'test second',
            'username': 'testuser2',
            'email': 'test@gmail.com',
            'password': 'test123',
            'password2': 'test123',
        }

        res = self.client.post(reverse('register'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'This email is beings used')
        self.assertRedirects(res, reverse('register'))

    def test_login_success_returns_message_and_redirects(self):
        payload = {
            'username': 'testuser',
            'password': 'test123'
        }

        res = self.client.post(reverse('login'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'you are now logged in')
        self.assertRedirects(res, reverse('dashboard'))

    def test_login_failed_returns_message_and_redirects(self):
        payload = {
            'username': 'testuserfail',
            'password': 'test123'
        }

        res = self.client.post(reverse('login'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid credentials')
        self.assertRedirects(res, reverse('login'))

    def test_logout_returns_message_and_redirects(self):
        res = self.client.post(reverse('logout'))
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'You are now logged out')
        self.assertRedirects(res, reverse('index'))

    def test_dashboard(self):
        res = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(res, 'accounts/dashboard.html')
