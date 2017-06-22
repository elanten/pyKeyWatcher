from django.http import HttpResponse
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from digital_key.models import *

from openpyxl.xml import constants

from employee.tests import create_group, create_employee


def create_key(name):
    return DigitalKey.objects.create(name=name)


def create_location(name):
    return KeyLocation.objects.create(name=name)


class DigitalKeyViewTest(TestCase):
    def test_all_empty(self):
        response = self.client.get(reverse('digital_key:all'))
        self.assertEqual(response.status_code, 200)

    def test_all(self):
        key1 = create_key('TEST KEY 1')
        key2 = create_key('TEST KEY 2')
        response = self.client.get(reverse('digital_key:all'))
        self.assertContains(response, key1.name)
        self.assertContains(response, key2.name)

    def test_show_by_id_view(self):
        key = create_key('Test key')
        response = self.client.get(reverse('digital_key:show_by_id', args=(key.id,)))
        self.assertContains(response, key.name)

    def test_export_xlsx(self):
        response: HttpResponse = self.client.get(reverse('digital_key:export_all_xlsx'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], constants.XLSX)


class KeyLocationViewTest(TestCase):
    def test_all_empty(self):
        response = self.client.get(reverse('digital_key:loc_all'))
        self.assertEqual(response.status_code, 200)

    def test_all(self):
        loc1 = create_location('TEST LOC 1')
        loc2 = create_location('TEST LOC 2')
        key = create_key('TEST KEY 1')
        key.location = loc1
        key.save()
        response = self.client.get(reverse('digital_key:loc_all'))
        self.assertContains(response, loc1.name)
        self.assertContains(response, loc2.name)

    def test_detail(self):
        loc = create_location('TEST LOC 1')
        grp = create_group('TEST GROUP 1')
        key = create_key('TEST KEY 1')
        key.location = loc
        key.employee_group = grp
        key.save()
        response = self.client.get(reverse('digital_key:loc_detail', args=(loc.id,)))
        self.assertContains(response, loc.name)
        self.assertContains(response, key.name)
