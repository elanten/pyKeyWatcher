from digitalkey.models import DigitalKey, KeyType, DigitalKeyContact, KeyAssignment
from contragent.models import Employee, ContactType, ContactInfo
from django.utils import dateparse

DigitalKeyContact.objects.all().delete()

DigitalKey.objects.all().delete()
KeyType.objects.all().delete()
KeyAssignment.objects.all().delete()

ContactInfo.objects.all().delete()
Employee.objects.all().delete()
ContactType.objects.all().delete()

eToken = KeyType.objects.create(name='eToken')
ruToken = KeyType.objects.create(name='ruToken')

email = ContactType.objects.create(name='почта')
phone = ContactType.objects.create(name='телефон')

loc1 = KeyAssignment(name='Госзакупки').save()
loc2 = KeyAssignment(name='Росаккредитация').save()

con1 = Employee.objects.create(name='Фамилия Имя Отчество', description='Описание')
con2 = Employee.objects.create(name='ООО Организация', description='Описание организации')

con3 = Employee.objects.create(name='Дьячкова Алла Куприяновна', description='Описание Дьячкова Алла Куприяновна')
con4 = Employee.objects.create(name='Матвеева Клавдия Иринеевна', description='Описание Матвеева Клавдия Иринеевна')
con5 = Employee.objects.create(name='Кулакова Жанна Богдановна', description='Описание Кулакова Жанна Богдановна')
con6 = Employee.objects.create(name='Медведьев Герман Валерьянович',
                               description='Описание Медведьев Герман Валерьянович')
con7 = Employee.objects.create(name='Блохина Кира Лукьяновна', description='Описание Блохина Кира Лукьяновна')
con8 = Employee.objects.create(name='Белоусова Евфросиния Агафоновна',
                               description='Описание Белоусова Евфросиния Агафоновна')
con9 = Employee.objects.create(name='Сергеев Кондрат Владленович', description='Описание Сергеев Кондрат Владленович')
con10 = Employee.objects.create(name='Колесников Мэлор Сергеевич', description='Описание Колесников Мэлор Сергеевич')
con11 = Employee.objects.create(name='Ларионова Иванна Улебовна', description='Описание Ларионова Иванна Улебовна')
con12 = Employee.objects.create(name='Яковлев Альвиан Матвеевич', description='Описание Яковлев Альвиан Матвеевич')
con13 = Employee.objects.create(name='ООО БГБ 123', description='Описание БайнетГамаБук')
con14 = Employee.objects.create(name='ООО БКИ', description='Описание БитКлавИнфо')
con15 = Employee.objects.create(name='ООО Qwe 123', description='Описание Quick Wild Eyes')


for con in Employee.objects.all():
    con.contactinfo_set.create(contact_type=email, value="test@test.io")
    con.contactinfo_set.create(contact_type=email, value="123 45 67")

key1 = DigitalKey.objects.create(
    name='Ключ 1', serial='SN-1111', expire=dateparse.parse_date('2017-05-30'),
    key_type=eToken, description='111', key_allocation=loc1
)
key2 = DigitalKey.objects.create(
    name='Ключ 2', serial='SN-2222', expire=dateparse.parse_date('2017-06-30'),
    key_type=eToken, description='222', key_allocation=loc2
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

DigitalKeyContact(type='h', digital_key=key1, contragent=con1).save()
DigitalKeyContact(type='c', digital_key=key1, contragent=con2).save()
DigitalKeyContact(type='h', digital_key=key2, contragent=con1).save()
DigitalKeyContact(type='c', digital_key=key2, contragent=con1).save()
DigitalKeyContact(type='c', digital_key=key2, contragent=con2).save()
