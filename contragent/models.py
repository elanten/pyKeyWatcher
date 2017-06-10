from django.db import models


# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def get_contact_info(self):
        return self.contactinfo_set.all()


class EmployeeGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    members = models.ManyToManyField(Employee, null=True)


class ContactType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    value = models.CharField(max_length=200)
    contact = models.ForeignKey(Employee, null=False)
    contact_type = models.ForeignKey(ContactType)
