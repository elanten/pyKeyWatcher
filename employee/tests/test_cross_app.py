from django.test import TestCase
from django.urls import reverse

from digital_key.tests.utils import create_key
from employee.tests.utils import create_group, create_employee


class EmployeeViewTest(TestCase):
    def test_detail(self):
        emp = create_employee('TEST-EMP-1')
        key = create_key('TEST-KEY-1')
        key.cert_holder = emp
        key.save()
        response = self.client.get(reverse('employee:show_by_id', args=(emp.id,)))
        self.assertContains(response, emp.name)
        self.assertContains(response, key.name)


class EmployeeGroupViewTest(TestCase):
    def test_url_list_cross(self):
        grp = create_group('TEST_GROUP_1')
        grp.members.add(create_employee('EMP1'), create_employee('EMP2'))
        grp.digitalkey_set.add(create_key('KEY1'))
        grp.save()
        response = self.client.get(reverse('employee:group_detail', args=(grp.id,)))
        self.assertContains(response, grp.name)
