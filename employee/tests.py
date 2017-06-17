from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from employee.models import *


def create_employee(name):
    return Employee.objects.create(name=name)


def create_group(name):
    return EmployeeGroup.objects.create(name=name)


class EmployeeViewTest(TestCase):
    def test_url_all(self):
        response = self.client.get(reverse('employee:all'))
        self.assertEqual(response.status_code, 200)

    def test_url_show_by_id(self):
        emp = create_employee('Test employee')
        response = self.client.get(reverse('employee:show_by_id', args=(emp.id,)))
        count = Employee.objects.count()
        self.assertContains(response, 'Test employee')
        self.assertEqual(count, 1)

    def test_url_json_by_name(self):
        create_employee('Emp test 1')
        create_employee('Emp test 2')
        create_employee('Emp 3')
        response = self.client.get(reverse('employee:json_by_name'), {'search': 'tes'})
        self.assertContains(response, 'Emp test 1')
        self.assertContains(response, 'Emp test 2')
        self.assertNotContains(response, 'Emp 3')


class EmployeeGroupViewTest(TestCase):
    def test_url_show_group_by_id(self):
        grp = create_group('Test group')
        response = self.client.get(reverse('employee:show_group_by_id', args=(grp.id,)))
        self.assertContains(response, 'Test group')
