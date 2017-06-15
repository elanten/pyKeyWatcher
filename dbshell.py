from digital_key.models import *
from employee.models import *
from cert_center.models import *
from key_manual.models import *
from django.utils import dateparse, timezone

c1 = ContactType(name='email')
c2 = ContactType(name='post')

c1.save()
c2.save()

emp1 = Employee(name='ФИО1')
emp2 = Employee(name='ФИО2')

emp1.save()
emp2.save()

emp1.contactinfo_set.create(value='test@mail.io', type=c1)
emp1.contactinfo_set.create(value='123 45 67', type=c2)

grp1 = EmployeeGroup.objects.create(name='Группа 1', description="1123")
grp1.members.add(emp1, emp2)

k1 = KeyType.objects.create(name="eToken")
k2 = KeyType.objects.create(name="ruToken")

ka1 = KeyAssignment.objects.create(name="Госсакупки")
ka2 = KeyAssignment.objects.create(name="Росчтототам")

kl1 = KeyLocation.objects.create(name="Склад 1")
kl2 = KeyLocation.objects.create(name="Склад 2")

cent1 = CertificationCenter.objects.create(name='Удостоверяющий центр 1',
                                           link='http://moscow.roskazna.ru/gis/uc',
                                           description='123')

cent2 = CertificationCenter.objects.create(name='Удостоверяющий центр 2', description='1234')

cr1 = CertRequirement.objects.create(name='Требования 1', center=cent1, description='123',
                                     actual_date=timezone.now())

key1 = DigitalKey(name="Ключ 1", serial='id-098765', type=k1, assignment=ka1, location=kl1, renewal_time=14,
                  cert_holder=emp1, key_receiver=emp1, employee_group=grp1, date_expire=timezone.now(),
                  cert_center=cent1)
key1.save()
key2 = DigitalKey(name="Ключ 2", serial='id-12345', type=k2, assignment=ka2, location=kl2, copy_of=key1)
key2.save()

mt1 = ManualType.objects.create(name='Установка')
mt2 = ManualType.objects.create(name='Использование')
mt3 = ManualType.objects.create(name='Ключи')

man1 = Manual.objects.create(name="Инструкция 1", type=mt1, content="Краткое описание\nинструкции",
                             link='http://www.roskazna.ru/gis/')
man2 = Manual.objects.create(name="Инструкция 2")
