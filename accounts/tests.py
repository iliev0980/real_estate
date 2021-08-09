from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from copy import deepcopy


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class UserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_register_page(self):
        res = self.client.get(reverse('register'))
        self.assertTemplateUsed(res, 'accounts/register.html')


    def test_creating_user(self):
        payload = {
            'first_name': 'test first',
            'last_name': 'test second',
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'test123',
            'password2': 'test123',
        }
        res = self.client.post(reverse('register'), payload)
        self.assertRedirects(res, reverse('login'))


    def test_passwords_doesnt_match_returns_message(self):
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




    def test_username_already_exists_returns_message(self):
        payload = {
            'first_name': 'test first',
            'last_name': 'test second',
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'test123',
            'password2': 'test123',
        }

        payload_clean = deepcopy(payload)
        payload_clean.popitem()
        create_user(**payload_clean)
        res = self.client.post(reverse('register'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'That username is taken')


    def test_email_already_exists_returns_message(self):
        payload = {
            'first_name': 'test first',
            'last_name': 'test second',
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'test123',
            'password2': 'test123',
        }

        payload_clean = deepcopy(payload)
        payload_clean['username'] = 'testuser2'
        payload_clean.popitem()
        create_user(**payload_clean)
        res = self.client.post(reverse('register'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'This email is beings used')

