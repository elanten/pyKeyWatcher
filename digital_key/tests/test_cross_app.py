from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse

from cert_center.tests.utils import create_cert_center
from digital_key.tests.utils import create_key, create_location, create_assignment
from employee.tests.utils import create_group, create_employee


class DigitalKeyView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='tester', password='123')

    def setUp(self):
        super().setUp()
        self.client.login(username='tester', password='123')

    def test_index_redirect(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/keys/')

    def test_url_detail_cross(self):
        loc = create_location('TEST LOC 1')
        emp_c = create_employee('TEST EMPLOYEE 1')
        emp_k = create_employee('TEST EMPLOYEE 2')
        grp = create_group('TEST GROUP 1')
        center = create_cert_center('TEST CERT CENT 1')
        asgn = create_assignment('TEST ASGN 1')

        key = create_key('TEST KEY 1')
        key.location = loc
        key.employee_group = grp
        key.cert_holder = emp_c
        key.key_receiver = emp_k
        key.cert_center = center
        key.assignment = asgn
        key.save()

        response = self.client.get(reverse('digital_key:show_by_id', args=(key.id,)))
        self.assertContains(response, key.name)
        self.assertContains(response, loc.name)
        self.assertContains(response, emp_c.name)
        self.assertContains(response, emp_k.name)
        self.assertContains(response, grp.name)
        self.assertContains(response, center.name)
        self.assertContains(response, asgn.name)
