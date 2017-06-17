from django.test import TestCase
from django.urls import reverse
from .models import *


# Create your tests here.

def create_manual(name):
    return Manual.objects.create(name=name)


class ManualViewTest(TestCase):
    def test_url_show_by_id(self):
        man = create_manual('TEST MANUAL')
        response = self.client.get(reverse('key_manual:show_by_id', args=(man.id,)))
        self.assertContains(response, 'TEST MANUAL')

    def test_url_show_all_empty(self):
        response = self.client.get(reverse('key_manual:all'))
        self.assertEqual(response.status_code, 200)

    def test_url_show_all(self):
        create_manual('TEST MANUAL')
        create_manual('TEST MANUAL')
        response = self.client.get(reverse('key_manual:all'))
        self.assertContains(response, 'TEST MANUAL', count=2)
