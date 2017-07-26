import logging

from django.db import models
from django.utils import timezone

from employee.models import Employee, EmployeeGroup
from cert_center.models import CertificationCenter

# Create your models here.


logger = logging.getLogger(__name__)


class KeyType(models.Model):
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class KeyLocation(models.Model):
    class Meta:
        verbose_name = 'Место хранения'
        verbose_name_plural = 'Места хранения'

    name = models.CharField(max_length=255)
    name_full = models.CharField(max_length=255, blank=True, default='')

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class WorkSystem(models.Model):
    class Meta:
        verbose_name = 'Используемые системы'
        verbose_name_plural = 'Используемые системы'

    name = models.CharField(max_length=255)
    name_full = models.CharField(max_length=255, blank=True, default='')

    description = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class KeyAssignment(models.Model):
    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'

    name = models.CharField(max_length=200)

    name_full = models.CharField(max_length=255, blank=True, default='')

    description = models.TextField(blank=True)

    work_systems = models.ManyToManyField(WorkSystem, blank=True)

    def __str__(self):
        return self.name


class DigitalKey(models.Model):
    class Meta:
        verbose_name = 'Ключ ЭЦП'
        verbose_name_plural = 'Ключи ЭЦП'

    name = models.CharField(max_length=255, verbose_name='Наименование')
    name_full = models.CharField(max_length=255, blank=True, default='')

    serial = models.CharField(max_length=200, verbose_name='Номер ключа')
    description = models.TextField(blank=True, null=True, default='', verbose_name='Описание')

    cert_num = models.CharField(max_length=255, blank=True, default='', verbose_name='Номер сертификата')

    pin_user = models.CharField(max_length=255, blank=True, default='')
    pin_admin = models.CharField(max_length=255, blank=True, default='')
    pin_container = models.CharField(max_length=255, blank=True, default='')

    date_begin = models.DateField(blank=True, null=True, verbose_name='Начало')
    date_expire = models.DateField(blank=True, null=True, verbose_name='Истекает')

    date_checked = models.DateField(blank=True, null=True, verbose_name='Проверен')

    renewal_time = models.PositiveIntegerField(blank=True, default=0, verbose_name="Срок перевыпуска")

    type = models.ForeignKey(KeyType, blank=True, null=True, verbose_name='Тип')
    assignment = models.ForeignKey(KeyAssignment, blank=True, null=True, verbose_name='Назначение')
    location = models.ForeignKey(KeyLocation, blank=True, null=True, verbose_name='Место хранения')

    cert_holder = models.ForeignKey(Employee, blank=True, null=True, related_name='cert_set', verbose_name='Владелец')
    key_receiver = models.ForeignKey(Employee, blank=True, null=True, related_name='key_set', verbose_name='Держатель')
    employee_group = models.ForeignKey(EmployeeGroup, blank=True, null=True, verbose_name='Группа держателей')

    cert_center = models.ForeignKey(CertificationCenter, blank=True, null=True, verbose_name='УЦ')

    work_systems = models.ManyToManyField(WorkSystem, blank=True, verbose_name='Поддерживаемые системы')

    copy_of = models.ForeignKey('DigitalKey', blank=True, null=True, verbose_name='Оригинал ключа',
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
