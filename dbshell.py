# Файл для работы с тестовой базой

from digital_key.models import *
from employee.models import *
from cert_center.models import *
from key_manual.models import *
from django.utils import dateparse, timezone
import re, random
import datetime as dt


def randomize_names():
    count = 1
    tpls = ['eTocken_{:02d}', 'ruTocken_{:02d}', 'Flash_{:02d}']
    tDict = {key: 0 for key in tpls}
    for key in DigitalKey.objects.all():
        key.serial = f'1234-xxx-{count:02d}'
        count += 1
        tpl: str = random.choice(tpls)
        pos = tDict[tpl] = tDict[tpl] + 1
        key.name = tpl.format(pos)
        key.save()
        count += 1


def randomize_dates():
    for key in DigitalKey.objects.all():
        now = dt.datetime.now()
        _start = now - dt.timedelta(days=random.randint(5, 10))
        _end = now + dt.timedelta(days=random.randint(15, 90))
        key.date_begin = _start.date()
        key.date_expire = _end.date()
        key.renewal_time = random.randint(5, 15)
        key.save()


def randomize_links():
    systems = [sys for sys in WorkSystem.objects.all()]
    assignments = [ass for ass in KeyAssignment.objects.all()]
    locs = [loc for loc in KeyLocation.objects.all()]
    types = [typ for typ in KeyType.objects.all()]
    centers = [cen for cen in CertificationCenter.objects.all()]
    employees = [emp for emp in Employee.objects.all()]
    for key in DigitalKey.objects.all():
        key.work_systems.add(random.choice(systems))
        key.assignment = random.choice(assignments)
        key.location = random.choice(locs)
        key.type = random.choice(types)
        key.cert_center = random.choice(centers)
        key.cert_holder = random.choice(employees)
        key.save()
