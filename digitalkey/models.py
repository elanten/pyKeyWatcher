from django.db import models
import datetime
from django.utils import timezone
from contragent.models import Contragent

import logging

# Create your models here.


logger = logging.getLogger(__name__)
dkc_types = (
    ('h', 'holder'),
    ('c', 'contact'),
)


class KeyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DigitalKey(models.Model):
    name = models.CharField(max_length=200)
    serial = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    expire = models.DateField()
    removed = models.BooleanField(default=False)
    key_type = models.ForeignKey(KeyType, null=True)
    contragent = models.ManyToManyField(
        Contragent,
        through='DigitalKeyContacts',
        through_fields=('digital_key', 'contragent')
    )

    def __str__(self):
        return self.name

    def get_holders(self):
        return self.contragent.filter(digitalkeycontacts__type='h')

    def get_contacts(self):
        return self.contragent.filter(digitalkeycontacts__type='c')

    @classmethod
    def get_keys_by_contact_id(cls, _id):
        DigitalKey.objects.filter(contragent__contragent_id=_id)

    def get_key_holders(self):
        return self.contragent.filter(digitalkeycontacts__type='h').distinct()

    def get_key_contacts(self):
        return self.contragent.filter(digitalkeycontacts__type='c').distinct()


class DigitalKeyContacts(models.Model):
    HOLDER = 'h'
    CONTACT = 'c'
    digital_key = models.ForeignKey(DigitalKey, on_delete=models.CASCADE)
    contragent = models.ForeignKey(Contragent, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=dkc_types)

    def __str__(self):
        return '%s %s %s' % (self.digital_key, self.contragent, self.type)
