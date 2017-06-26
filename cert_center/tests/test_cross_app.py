from django.test import TestCase
from django.urls import reverse

from cert_center.tests.utils import create_cert_center, create_cert_requirement
from digital_key.tests.utils import create_key, create_location


class CertCenterViewTest(TestCase):
    def test_url_detail_cross(self):
        req1 = create_cert_requirement('TEST_REQ_1')
        req2 = create_cert_requirement('TEST_REQ_2')
        loc1 = create_location('TEST_LOC_1')
        loc2 = create_location('TEST_LOC_2')
        key1 = create_key('TEST_KEY_1')
        key2 = create_key('TEST_KEY_2')
        key1.location = loc1
        key1.save()
        key2.location = loc2
        key2.save()
        center = create_cert_center('TEST_CERT_CENT')
        center.certrequirement_set.add(req1, req2)
        center.digitalkey_set.add(key1, key2)

        response = self.client.get(reverse('cert_center:show_by_id', args=(center.id,)))
        self.assertContains(response, center.name)
        self.assertContains(response, req1.name)
        self.assertContains(response, req2.name)
        self.assertContains(response, key1.name)
        self.assertContains(response, key2.name)
        self.assertContains(response, loc1.name)
        self.assertContains(response, loc2.name)
