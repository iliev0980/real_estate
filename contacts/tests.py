from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
import tempfile
from listings.models import Listing
from realtors.models import Realtor
from .models import Contact

def create_user(name):
    payload = {
        'first_name': 'test first',
        'last_name': 'test second',
        'username': f'testuser{name}',
        'email': f'test{name}@gmail.com',
        'password': 'test123',
    }
    return get_user_model().objects.create_user(**payload)

def create_contact(name):
    user = create_user(name)
    listing = create_listing(name)
    payload = {
        'listing': listing,
        'listing_id': listing.id,
        'name': 'testName',
        'email': 'testemail@gmail.com',
        'phone': '123456789',
        'message': 'test message',
        'contact_date': '2011-11-11',
        'user_id': user.id,
    }
    return Contact.objects.create(**payload)


def create_realtor(name):
    payload = {
        'name': f'testRealtor{name}',
        'photo': tempfile.NamedTemporaryFile(suffix=".jpg").name,
        'description': 'some description',
        'phone': '123456789',
        'email': f'testEmail{name}@gmail.com',
        'is_mvp': 'False',
        'hire_date': '2012-12-12'
    }
    return Realtor.objects.create(**payload)


def create_listing(name):
    realtor = create_realtor(name)
    payload = {
        'realtor': realtor,
        'title': f'Test Property {name}',
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


class ContactTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.contact = create_contact('setup')

    def test_creating_contact_not_authenticated_user_success(self):
        listing = create_listing('testListing')
        payload = {
            'listing': listing.title,
            'listing_id': listing.id,
            'name': 'testName',
            'email': 'testemail@gmail.com',
            'phone': '123456789',
            'message': 'test message',
            'contact_date': '2011-11-11',
            'user_id': '0',
            'realtor_email': listing.realtor.email
        }
        res = self.client.post(reverse('contact'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your request has benn submitted, a realtor will get back to you soon')
        self.assertRedirects(res, reverse('listings') + str(listing.id))


    def test_creating_contact_authenticated_user_success(self):
        listing = create_listing('testListing')
        payload = {
            'listing': listing.title,
            'listing_id': listing.id,
            'name': 'testName',
            'email': 'testemail@gmail.com',
            'phone': '123456789',
            'message': 'test message',
            'contact_date': '2011-11-11',
            'user_id': '0',
            'realtor_email': listing.realtor.email
        }
        self.client.login(username='testusersetup', password='test123')
        res = self.client.post(reverse('contact'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your request has benn submitted, a realtor will get back to you soon')
        self.assertRedirects(res, reverse('listings') + str(listing.id))

    def test_creating_existing_contact(self):
        payload = {
            'listing': self.contact.listing.title,
            'listing_id': self.contact.listing_id,
            'name': 'testName',
            'email': 'testemail@gmail.com',
            'phone': '123456789',
            'message': 'test message',
            'contact_date': '2011-11-11',
            'user_id': self.contact.user_id,
            'realtor_email': self.contact.listing.realtor.email
        }
        self.client.login(username='testusersetup', password='test123')
        res = self.client.post(reverse('contact'), payload)
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(str(messages[0]), 'You have already made an inquiry for this listing')
        self.assertRedirects(res, reverse('listings') + str(self.contact.listing_id))