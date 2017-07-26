import datetime

from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from django.views import generic

from digital_key.support import DigitalKeyWrapper
from employee.forms import *
from digital_key.models import DigitalKey
from .models import Employee, ContactInfo, EmployeeGroup


# Create your views here.
class KeyListWrapper:
    def __init__(self, employee):
        keys = {}

        for key in employee.cert_set.all():
            keys[key.pk] = EmployeeKeyWrapper(key, in_cert=True)

        for key in employee.key_set.all():
            wkey = keys.get(key.pk, EmployeeKeyWrapper(key))
            wkey.in_hold = True
            keys[key.pk] = wkey

        grp_ids = employee.employeegroup_set.values('id')
        for key in DigitalKey.objects.filter(employee_group__in=grp_ids):
            wkey = keys.get(key.pk, EmployeeKeyWrapper(key))
            wkey.in_group = True
            keys[key.pk] = wkey

        self.keys = keys

    def __iter__(self):
        return iter(sorted(
            self.keys.values(),
            key=lambda e: (e.key.date_expire if e.key.date_expire else datetime.date(9999, 1, 1))
        ))


class EmployeeKeyWrapper(DigitalKeyWrapper):
    def __init__(self, digital_key: DigitalKey, in_cert=False, in_hold=False, in_group=False):
        super(EmployeeKeyWrapper, self).__init__(digital_key, default_style='success')
        self.in_cert = in_cert
        self.in_hold = in_hold
        self.in_group = in_group


class EmployeeListView(generic.ListView):
    model = Employee
    template_name = 'employee/emp_list.html'
    context_object_name = 'employees'
    allow_empty = True


# def show_all(request):
#     return render(request, 'employee/key_list.html', {
#         'employees': Employee.objects.all()
#     })


def show_by_id(request, cid: int):
    employee = get_object_or_404(Employee, pk=cid)
    cert_keys = DigitalKey.objects.filter(cert_holder=employee).order_by('date_expire')
    wrapped_list = KeyListWrapper(employee)
    return render(request, 'employee/emp_detail.html', {
        'employee': employee,
        'groups': employee.employeegroup_set.all(),
        'key_views': (DigitalKeyWrapper(key) for key in cert_keys)
    })


def show_group_by_id(request, pk):
    group = get_object_or_404(EmployeeGroup, pk=pk)
    members = group.members.all()
    wrp_keys = (DigitalKeyWrapper(key) for key in group.digitalkey_set.all())
    return render(request, 'employee/group_detail.html', {
        'group': group,
        'members': members,
        'wrp_keys': wrp_keys
    })


def show_all_by_type(request, ctype):
    employees = Employee.objects.filter(digitalkeycontact__type=ctype[:1]).distinct()
    if not employees:
        raise Http404('Контакты')
    return render(request, 'employee/emp_list.html', {
        'employees': employees
    })


def edit_by_id(request, cid: int):
    employee = get_object_or_404(Employee, pk=cid)
    info_set = employee.contactinfo_set.all()
    ContactInfoFormSet = modelformset_factory(
        ContactInfo, form=EmployeeDetailForm,
        extra=0, can_delete=True)
    if request.method == 'POST':
        contragent_form = EmployeeForm(request.POST, instance=employee)
        info_formset = ContactInfoFormSet(request.POST, queryset=info_set)
        if contragent_form.is_valid() and info_formset.is_valid():
            if contragent_form.has_changed():
                employee = contragent_form.save()
            if info_formset.has_changed():
                info_formset.save_existing_objects()
                info_formset.saved_forms = []
                for contact_info in info_formset.save_new_objects(commit=False):
                    contact_info.contact = employee
                    contact_info.save()
            return redirect('employee:show_by_id', employee.id)
    else:
        contragent_form = EmployeeForm(instance=employee)
        info_formset = ContactInfoFormSet(queryset=info_set)

    return render(request, 'employee/emp_edit.html', {
        'contragent_form': contragent_form,
        'info_formset': info_formset
    })


def create(request):
    ContactInfoFormSet = formset_factory(EmployeeDetailForm, extra=1, can_delete=True)
    if request.method == 'POST':
        contragent_form = EmployeeForm(request.POST)
        info_formset = ContactInfoFormSet(request.POST)
        if contragent_form.is_valid():
            contragent = contragent_form.save()
            if info_formset.is_valid():
                for form in info_formset.forms:
                    contact_info = form.save(commit=False)
                    contact_info.contact = contragent
                    contact_info.save()
            return redirect('employee:show_by_id', contragent.id)
    else:
        contragent_form = EmployeeForm()
        info_formset = ContactInfoFormSet()
    return render(request, 'employee/emp_edit.html', {
        'contragent_form': contragent_form,
        'info_formset': info_formset
    })


def remove_by_id(request, cid):
    employee = get_object_or_404(Employee, pk=cid)
    employee.delete()
    return redirect('employee:all')


def show_all_by_name(request):
    if request.method == 'GET':
        form = ContragentSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['search']
            agents = Employee.objects.filter(name__icontains=name).values('id', 'name')
            response = JsonResponse(list(agents), safe=False)
            return response
    else:
        return JsonResponse({})


class EmployeeGroupsList(generic.ListView):
    model = EmployeeGroup
    template_name = 'employee/group_list.html'
    context_object_name = 'groups'
    allow_empty = True


def group_all(request):
    groups = EmployeeGroup.objects.all()

    return None
