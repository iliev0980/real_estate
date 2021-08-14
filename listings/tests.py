from django.test import TestCase
from django.test import Client
from django.urls import reverse
from listings.models import Listing
from realtors.models import Realtor
import tempfile


def create_listing():
    realtor = create_realtor()
    payload = {
        'realtor': realtor,
        'title': f'Test Property',
        'address': f'test adrres',
        'city': f'testCity',
        'state': f'testState',
        'zipcode': '1234',
        'price': '12345',
        'bedrooms': '1',
        'bathrooms': '2',
        'sqft': '123',
        'lot_size': '1',
        'photo_main': tempfile.NamedTemporaryFile(suffix=".jpg").name,
    }
    return Listing.objects.create(**payload)


def create_realtor():
    payload = {
        'name': f'testRealtor',
        'photo': tempfile.NamedTemporaryFile(suffix=".jpg").name,
        'description': 'some description',
        'phone': '123456789',
        'email': f'testEmail@gmail.com',
        'is_mvp': 'False',
        'hire_date': '2012-12-12'
    }
    return Realtor.objects.create(**payload)


class ListingsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.listing = create_listing()

    def test_get_listings_page(self):
        res = self.client.get(reverse('listings'))
        self.assertTemplateUsed(res, 'listings/listings.html')




