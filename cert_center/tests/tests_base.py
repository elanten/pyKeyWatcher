from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from cert_center.tests.utils import create_cert_center, create_cert_requirement


class CertificationCenterViewTest(TestCase):
    def test_url_show_by_id(self):
        center = create_cert_center('Test center')
        response = self.client.get(reverse('cert_center:show_by_id', args=(center.id,)))
        self.assertContains(response, 'Test center')

    def test_url_show_all_empty(self):
        response = self.client.get(reverse('cert_center:all'))
        self.assertEqual(response.status_code, 200)

    def test_url_show_all(self):
        create_cert_center('Test 1')
        create_cert_center('Test 2')
        response = self.client.get(reverse('cert_center:all'))
        self.assertContains(response, 'Test 1')
        self.assertContains(response, 'Test 2')


class CertRequirementViewTest(TestCase):
    def test_url_show_by_id(self):
        req = create_cert_requirement('TEST REQ')
        response = self.client.get(reverse('cert_center:show_req_by_id', args=(req.id,)))
        self.assertContains(response, 'TEST REQ')
