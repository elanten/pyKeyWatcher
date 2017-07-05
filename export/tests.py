from django.contrib.auth.models import User
from django.test import TestCase
from openpyxl.xml import constants
# Create your tests here.
from django.urls import reverse


class ExportTestNoLogin(TestCase):
    def test_export_xlsx(self):
        response = self.client.get(reverse('export:xlsx'))
        self.assertEqual(response.status_code, 302)


class ExportTestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='tester', password='pass-123')

    def setUp(self):
        super().setUp()
        self.client.login(username='tester', password='pass-123')

    def test_export_xlsx(self):
        response = self.client.get(reverse('export:xlsx'))
        self.assertEqual(response.status_code, 302)


class ExportTestStaff(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_superuser('su-test', 'email@test.io', 'pass-123')

    def setUp(self):
        super().setUp()
        self.client.login(username='su-test', password='pass-123')

    def test_export_xlsx(self):
        response = self.client.get(reverse('export:xlsx'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], constants.XLSX)
