from django.test import TestCase
from openpyxl.xml import constants
# Create your tests here.
from django.urls import reverse


class ExportTest(TestCase):
    def test_export_xlsx(self):
        response = self.client.get(reverse('export:xlsx'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], constants.XLSX)