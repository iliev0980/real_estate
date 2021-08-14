from django.test import TestCase
from django.test import Client
from django.urls import reverse

class PagesTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_index_page(self):
        res = self.client.get(reverse('index'))
        self.assertTemplateUsed(res, 'pages/index.html')

    def test_get_about_page(self):
        res = self.client.get(reverse('about'))
        self.assertTemplateUsed(res, 'pages/about.html')
