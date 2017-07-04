from django.db import models


# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=255)
    name_full = models.CharField(max_length=255, blank=True, default='')

    description = models.TextField(blank=True, default="")

    def get_contact_info(self):
        return self.contactinfo_set.all()

    def __str__(self):
        return self.name


class EmployeeGroup(models.Model):
    name = models.CharField(max_length=255)
    name_full = models.CharField(max_length=255, blank=True, default='')

    description = models.TextField(blank=True, default="")
    members = models.ManyToManyField(Employee)

    def __str__(self):
        return self.name


class ContactType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    type = models.ForeignKey(ContactType)
    value = models.CharField(max_length=200)

    employee = models.ForeignKey(Employee)

    def __str__(self):
        return self.value
