from digitalkey.models import DigitalKey, KeyType, DigitalKeyContacts
from contragent.models import Contragent, ContactType, ContactInfo
from django.utils import dateparse

DigitalKeyContacts.objects.all().delete()

DigitalKey.objects.all().delete()
KeyType.objects.all().delete()

ContactInfo.objects.all().delete()
Contragent.objects.all().delete()
ContactType.objects.all().delete()

eToken = KeyType.objects.create(name='eToken')
ruToken = KeyType.objects.create(name='ruToken')

email = ContactType.objects.create(name='почта')
phone = ContactType.objects.create(name='телефон')

con1 = Contragent.objects.create(name='ФИО 1', description='123')
con2 = Contragent.objects.create(name='ООО 1', description='456')

con1.contactinfo_set.create(contact_type=email, value='test@test.io')
con1.contactinfo_set.create(contact_type=phone, value='123 45 67')

con2.contactinfo_set.create(contact_type=email, value='test@test.io')
con2.contactinfo_set.create(contact_type=phone, value='123 45 67')

key1 = DigitalKey.objects.create(
    name='Ключ 1', serial='SN-1111', expire=dateparse.parse_date('2017-05-30'),
    key_type=eToken, description='111'
)
key2 = DigitalKey.objects.create(
    name='Ключ 2', serial='SN-2222', expire=dateparse.parse_date('2017-06-30'),
    key_type=eToken, description='222'
)
key3 = DigitalKey.objects.create(
    name='Ключ 3', serial='SN-3333', expire=dateparse.parse_date('2017-07-30'),
    key_type=eToken, description='333'
)
key4 = DigitalKey.objects.create(
    name='Ключ 4', serial='SN-4444', expire=dateparse.parse_date('2017-08-30'),
    key_type=eToken, description='444'
)
key5 = DigitalKey.objects.create(
    name='Ключ 5', serial='SN-5555', expire=dateparse.parse_date('2017-09-30'),
    key_type=eToken, description='555'
)

DigitalKeyContacts.objects.create(type='h', digital_key=key1, contragent=con1).save()
DigitalKeyContacts.objects.create(type='c', digital_key=key1, contragent=con2).save()
DigitalKeyContacts.objects.create(type='h', digital_key=key2, contragent=con1).save()
DigitalKeyContacts.objects.create(type='c', digital_key=key2, contragent=con1).save()
DigitalKeyContacts.objects.create(type='c', digital_key=key2, contragent=con2).save()
