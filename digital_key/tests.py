from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from digital_key.models import DigitalKey


def create_key(name):
    return DigitalKey.objects.create(name=name)


class DigitalKeyViewTest(TestCase):
    def test_all_view(self):
        response = self.client.get(reverse('digital_key:all'))
        self.assertEqual(response.status_code, 200)

    def test_show_by_id_view(self):
        key = create_key('Test key')
        response = self.client.get(reverse('digital_key:show_by_id', args=(key.id,)))
        self.assertContains(response, 'Test key')
