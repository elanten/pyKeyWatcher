from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from django.urls import reverse

from digital_key.tests.utils import create_key, create_location, create_work_system

URL_DIGITAL_KEY_ALL = 'digital_key:all'
URL_DIGITAL_KEY_DETAIL = 'digital_key:show_by_id'
URL_LOCATION_ALL = 'digital_key:loc_all'
URL_LOCATION_DETAIL = 'digital_key:loc_detail'
URL_SYSTEM_ALL = 'digital_key:sys_all'
URL_SYSTEM_DETAIL = 'digital_key:sys_detail'


class DigitalKeyViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='tester', password='123')

    def setUp(self):
        super().setUp()
        self.client.login(username='tester', password='123')

    def test_all_empty(self):
        response = self.client.get(reverse(URL_DIGITAL_KEY_ALL))
        self.assertEqual(response.status_code, 200)

    def test_all(self):
        key1 = create_key('TEST KEY 1')
        key2 = create_key('TEST KEY 2')
        response = self.client.get(reverse(URL_DIGITAL_KEY_ALL))
        self.assertContains(response, key1.name)
        self.assertContains(response, key2.name)

    def test_url_detail_simple(self):
        key = create_key('Test key')
        response = self.client.get(reverse(URL_DIGITAL_KEY_DETAIL, args=(key.id,)))
        self.assertContains(response, key.name)

    def test_url_detail_complex(self):
        loc = create_location('TEST-LOC-1')
        sys = create_work_system('TEST-SYS-1')
        key = create_key('TEST-KEY-1')
        key.pin_container = 'PIN-CON-123'
        key.pin_admin = 'PIN-ADM-123'
        key.pin_user = 'PIN-USR-123'
        key.location = loc
        key.work_systems.add(sys)
        key.save()
        key_url = reverse(URL_DIGITAL_KEY_DETAIL, args=(key.id,))
        response = self.client.get(key_url)
        loc_url = reverse(URL_LOCATION_DETAIL, args=(loc.id,))
        sys_url = reverse(URL_SYSTEM_DETAIL, args=(sys.id,))

        self.assertContains(response, key.name)
        self.assertContains(response, loc.name)
        self.assertContains(response, loc_url)
        self.assertContains(response, sys.name)
        self.assertContains(response, sys_url)

        self.assertNotContains(response, key.pin_container)
        self.assertNotContains(response, key.pin_admin)
        self.assertNotContains(response, key.pin_user)


class DigitalKeyViewTestNoLogin(TestCase):
    # w/o logged in
    def test_all_empty(self):
        response = self.client.get(reverse(URL_DIGITAL_KEY_ALL))
        self.assertEquals(response.status_code, 302)

    def test_all(self):
        key1 = create_key('TEST KEY 1')
        key2 = create_key('TEST KEY 2')
        response = self.client.get(reverse(URL_DIGITAL_KEY_ALL))
        self.assertEquals(response.status_code, 302)

    def test_url_detail_simple(self):
        key = create_key('Test key')
        response = self.client.get(reverse(URL_DIGITAL_KEY_DETAIL, args=(key.id,)))
        self.assertEquals(response.status_code, 302)


class DigitalKeyViewTestStaff(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_superuser(
            username='su-tester',
            password='su-pass',
            email='email@test.io'
        )

    def setUp(self):
        super().setUp()
        self.client.login(username='su-tester', password='su-pass')

    def test_detail_complex(self):
        loc = create_location('TEST-LOC-1')
        sys = create_work_system('TEST-SYS-1')
        key = create_key('TEST-KEY-1')
        key.pin_container = 'PIN-CON-123'
        key.pin_admin = 'PIN-ADM-123'
        key.pin_user = 'PIN-USR-123'
        key.location = loc
        key.work_systems.add(sys)
        key.save()
        key_url = reverse(URL_DIGITAL_KEY_DETAIL, args=(key.id,))
        response = self.client.get(key_url)
        loc_url = reverse(URL_LOCATION_DETAIL, args=(loc.id,))
        sys_url = reverse(URL_SYSTEM_DETAIL, args=(sys.id,))

        self.assertContains(response, key.name)
        self.assertContains(response, loc.name)
        self.assertContains(response, loc_url)
        self.assertContains(response, sys.name)
        self.assertContains(response, sys_url)

        self.assertContains(response, key.pin_container)
        self.assertContains(response, key.pin_admin)
        self.assertContains(response, key.pin_user)


class KeyLocationViewTest(TestCase):
    def test_all_empty(self):
        response = self.client.get(reverse(URL_LOCATION_ALL))
        self.assertEqual(response.status_code, 200)

    def test_all(self):
        loc1 = create_location('TEST LOC 1')
        loc2 = create_location('TEST LOC 2')
        key = create_key('TEST KEY 1')
        key.location = loc1
        key.save()
        response = self.client.get(reverse(URL_LOCATION_ALL))
        self.assertContains(response, loc1.name)
        self.assertContains(response, loc2.name)

    def test_detail(self):
        loc = create_location('TEST LOC 1')
        key = create_key('TEST KEY 1')
        key.location = loc
        key.save()
        response = self.client.get(reverse(URL_LOCATION_DETAIL, args=(loc.id,)))
        self.assertContains(response, loc.name)
        self.assertContains(response, key.name)


class WorkSystemsTest(TestCase):
    def test_url_all_empty(self):
        response = self.client.get(reverse(URL_SYSTEM_ALL))
        self.assertEqual(response.status_code, 200)

    def test_url_all(self):
        create_work_system('TEST-WORK-SYS-1')
        create_work_system('TEST-WORK-SYS-2')
        response = self.client.get(reverse(URL_SYSTEM_ALL))
        self.assertContains(response, 'TEST-WORK-SYS', count=2)

    def test_url_detail_404(self):
        response = self.client.get(reverse(URL_SYSTEM_DETAIL, args=(99999,)))
        self.assertEqual(response.status_code, 404)

    def test_url_detail(self):
        sys = create_work_system('TEST-SYS-1')
        response = self.client.get(reverse(URL_SYSTEM_DETAIL, args=(sys.id,)))
        self.assertContains(response, sys.name)
