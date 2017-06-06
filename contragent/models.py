from django.db import models
from typing import List

# Create your models here.


class Contragent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    removed = models.BooleanField(default=False)

    def get_contact_info(self):
        return self.contactinfo_set.all()


class ContactType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    value = models.CharField(max_length=200)
    contact = models.ForeignKey(Contragent, null=False)
    contact_type = models.ForeignKey(ContactType)
