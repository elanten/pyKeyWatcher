from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from employee.forms import *
from  digitalkey.models import DigitalKey
from digitalkey.support import EmployeeKeyWrapper
from .models import Employee, ContactInfo


# Create your views here.
class EmployeeWrapper:
    def __init__(self, employee):
        self.employee = employee

    def cert_set(self):
        return self.employee.cert_set.all()

    def key_set(self):
        return self.employee.key_set.all()

    def group_set(self):
        grp_ids = self.employee.employeegroup_set.values('id')
        return DigitalKey.objects.filter(employee_group__in=grp_ids)


def show_all(request):
    return render(request, 'employee/list.html', {
        'employees': get_list_or_404(Employee)
    })


def show_by_id(request, cid: int):
    employee = get_object_or_404(Employee, pk=cid)
    # linked_keys_gen = (EmployeeKeyWrapper(employee, key) for key in employee.digitalkey_set.distinct())
    return render(request, 'employee/detail.html', {
        'view': EmployeeWrapper(employee),
        # 'linked_keys': linked_keys_gen
    })


def show_all_by_type(request, ctype):
    employees = Employee.objects.filter(digitalkeycontact__type=ctype[:1]).distinct()
    if not employees:
        raise Http404('Контакты')
    return render(request, 'employee/list.html', {
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

    return render(request, 'employee/edit.html', {
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
    return render(request, 'employee/edit.html', {
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
