from django.db import models
import datetime
from django.utils import timezone
from contragent.models import Employee

import logging

# Create your models here.


logger = logging.getLogger(__name__)


class KeyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class KeyAssignment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class DigitalKey(models.Model):
    name = models.CharField(max_length=200)
    serial = models.CharField(max_length=200)
    description = models.TextField(null=True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    type = models.ForeignKey(KeyType, null=True)
    assignment = models.ForeignKey(KeyAssignment, null=True)
    cert_holder = models.ForeignKey(Employee, null=True)
    key_receiver = models.ForeignKey(Employee, null=True)


    # contacts = models.ManyToManyField(
    #     Contragent,
    #     through='DigitalKeyContact',
    #     through_fields=('digital_key', 'contragent')
    # )

    def __str__(self):
        return self.name

    def get_holders(self):
        return self.contacts.filter(digitalkeycontact__type=DigitalKeyContact.HOLDER)

    def get_contacts(self):
        return self.contacts.filter(digitalkeycontact__type=DigitalKeyContact.CONTACT)

    @classmethod
    def get_keys_by_contact_id(cls, _id):
        DigitalKey.objects.filter(contragent__contragent_id=_id)

    def get_key_holders(self):
        return self.contacts.filter(digitalkeycontact__type=DigitalKeyContact.HOLDER).distinct()

    def get_key_contacts(self):
        return self.contacts.filter(digitalkeycontact__type=DigitalKeyContact.CONTACT).distinct()


class DigitalKeyContact(models.Model):
    HOLDER = 'h'
    CONTACT = 'c'
    _dkc_types = (
        (HOLDER, 'holder'),
        (CONTACT, 'contact'),
    )

    digital_key = models.ForeignKey(DigitalKey, on_delete=models.CASCADE)
    contragent = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=_dkc_types)

    def __str__(self):
        return '%s %s %s' % (self.digital_key, self.contragent, self.type)
