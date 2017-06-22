from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from employee.models import *


def create_employee(name):
    return Employee.objects.create(name=name)


def create_group(name):
    return EmployeeGroup.objects.create(name=name)


class EmployeeViewTest(TestCase):
    def test_url_all_empty(self):
        response = self.client.get(reverse('employee:all'))
        self.assertEqual(response.status_code, 200)

    def test_url_all(self):
        create_employee('TEST EMP 1')
        create_employee('TEST EMP 2')
        response = self.client.get(reverse('employee:all'))
        self.assertContains(response, 'TEST EMP 1')
        self.assertContains(response, 'TEST EMP 2')

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
    def test_url_group_detail(self):
        grp = create_group('Test group')
        response = self.client.get(reverse('employee:group_detail', args=(grp.id,)))
        self.assertContains(response, 'Test group')

    def test_url_all_none(self):
        response = self.client.get(reverse('employee:group_all'))
        self.assertEqual(response.status_code, 200)

    def test_url_all(self):
        grp1 = create_group('TEST_GROUP_1')
        grp2 = create_group('TEST_GROUP_2')
        response = self.client.get(reverse('employee:group_all'))
        self.assertContains(response, grp1.name)
        self.assertContains(response, grp2.name)
