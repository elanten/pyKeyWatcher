import logging

from django.db import models
from django.utils import timezone

from employee.models import Employee, EmployeeGroup
from cert_center.models import CertificationCenter

# Create your models here.


logger = logging.getLogger(__name__)


class KeyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class KeyAssignment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class KeyLocation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DigitalKey(models.Model):
    name = models.CharField(max_length=255)
    serial = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True, default='')

    pin_user = models.CharField(max_length=255, blank=True, default='')
    pin_admin = models.CharField(max_length=255, blank=True, default='')
    pin_container = models.CharField(max_length=255, blank=True, default='')

    date_begin = models.DateField(blank=True, null=True)
    date_expire = models.DateField(blank=True, null=True)
    renewal_time = models.PositiveIntegerField(blank=True, default=0)

    type = models.ForeignKey(KeyType, blank=True, null=True)
    assignment = models.ForeignKey(KeyAssignment, blank=True, null=True)
    location = models.ForeignKey(KeyLocation, blank=True, null=True)

    cert_holder = models.ForeignKey(Employee, blank=True, null=True, related_name='cert_set')
    key_receiver = models.ForeignKey(Employee, blank=True, null=True, related_name='key_set')
    employee_group = models.ForeignKey(EmployeeGroup, blank=True, null=True)

    cert_center = models.ForeignKey(CertificationCenter, blank=True, null=True)

    copy_of = models.ForeignKey('DigitalKey', blank=True, null=True,
                                on_delete=models.SET_NULL,
                                limit_choices_to={'copy_of': None})

    def get_copies(self):
        return DigitalKey.objects.filter(copy_of=self)

    def is_copy(self):
        return bool(self.copy_of)

    def days_left(self):
        if self.date_expire:
            delta = self.date_expire - timezone.now().date()
            return delta.days
        else:
            return 0

    def __str__(self):
        return self.name
