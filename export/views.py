from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet import Worksheet
from openpyxl.writer.excel import save_virtual_workbook

from digital_key.models import DigitalKey
from digital_key.views import _to_string


def export_key_xlsx(request):
    wb = Workbook()

    alignment = Alignment(horizontal='center', vertical='center')
    bold = Font(bold=True)

    ws: Worksheet = wb.active
    ws.title = 'Ключи'
    ws.append(['Назначение', 'номер', 'тип', 'имя', 'начало', 'конец', 'фио',
               'выдан', 'группа', 'уц', 'хранение', 'описание', 'оригинал', 'системы'])

    for cell in ws[1]:
        cell.font = bold
        cell.alignment = alignment

    for key in DigitalKey.objects.all():
        _ass = _to_string(key.assignment)
        _ser = _to_string(key.serial)
        _typ = _to_string(key.type)
        _nam = _to_string(key.name)
        _beg = key.date_begin
        _exp = key.date_expire
        _cer = _to_string(key.cert_holder)
        _rec = _to_string(key.key_receiver)
        _emp = _to_string(key.employee_group)
        _cen = _to_string(key.cert_center)
        _loc = _to_string(key.location)
        _des = _to_string(key.description)
        _cop = _to_string(key.copy_of.serial) if key.copy_of else None
        _sys = ', '.join(sys.name for sys in key.work_systems.all())
        ws.append([_ass, _ser, _typ, _nam, _beg, _exp, _cer, _rec, _emp, _cen, _loc, _des, _cop, _sys])

    # ws['A1'] = 42
    #
    # # Rows can also be appended
    # ws.append(['ключ 1', 2, 3])
    # ws.append(['ключ 1', 2, 3])
    # ws.merge_cells('A2:A3')
    # ws.append(['ключ 2', 2, 3])
    # # Python types will automatically be converted
    # import datetime
    #
    # ws['A4'] = datetime.datetime.now()

    # fix column width
    for column_cells in ws.columns:
        length = max(len(_to_string(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column].width = length + 2

    response = HttpResponse(save_virtual_workbook(wb), content_type=wb.mime_type)
    response['Content-Disposition'] = 'attachment; filename="keys.xlsx"'

    return response
