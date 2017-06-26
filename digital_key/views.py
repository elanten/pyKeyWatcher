from django.core.handlers.wsgi import WSGIHandler
from django.shortcuts import render, get_object_or_404, redirect

from .forms import DigitalKeyForm
from .models import DigitalKey, KeyLocation, WorkSystem
from .support import DigitalKeyWrapper


def _to_string(obj, default=''):
    return str(obj) if obj else default


def show_all(request):
    keys = DigitalKey.objects.all()
    key_views = list(DigitalKeyWrapper(key) for key in keys)
    return render(request, 'digital_key/list.html', {
        'key_views': key_views
    })


def show_by_id(request, key_id):
    digital_key = get_object_or_404(DigitalKey, pk=key_id)
    return render(request, 'digital_key/detail.html', {
        'view': DigitalKeyWrapper(digital_key)
    })


def edit_by_id(request: WSGIHandler, key_id):
    digital_key = get_object_or_404(DigitalKey, pk=key_id)
    # holders = digital_key.contacts.filter(digitalkeycontact__type=DigitalKeyContact.HOLDER).values('id', 'name')
    # contacts = digital_key.contacts.filter(digitalkeycontact__type=DigitalKeyContact.CONTACT).values('id', 'name')

    if request.method == 'POST':
        digital_key_form = DigitalKeyForm(request.POST, instance=digital_key)
        if digital_key_form.is_valid():
            if digital_key_form.has_changed():
                digital_key = digital_key_form.save()
            digital_key.contacts.clear()
            holders_ids = request.POST.getlist('holders', [])
            contacts_ids = request.POST.getlist('contacts', [])
            # for _id in holders_ids:
            #     DigitalKeyContact(digital_key=digital_key, contragent_id=_id,
            #                       type=DigitalKeyContact.HOLDER).save()
            #
            # for _id in contacts_ids:
            #     DigitalKeyContact(digital_key=digital_key, contragent_id=_id,
            #                       type=DigitalKeyContact.CONTACT).save()
            return redirect('digital_key:show_by_id', digital_key.id)
    else:
        digital_key_form = DigitalKeyForm(instance=digital_key)

    return render(request, 'digital_key/edit.html', {
        'digitalkey_form': digital_key_form,
        # 'holders': holders,
        # 'contacts': contacts
    })


def create(request):
    digital_key = DigitalKey()
    if request.method == 'POST':
        digital_key_form = DigitalKeyForm(request.POST, instance=digital_key)
        if digital_key_form.is_valid():
            digital_key = digital_key_form.save()
            holders_ids = request.POST.getlist('holders', [])
            contacts_ids = request.POST.getlist('contacts', [])
            # for _id in holders_ids:
            #     DigitalKeyContact(digital_key=digital_key, contragent_id=_id,
            #                       type=DigitalKeyContact.HOLDER).save()
            # for _id in contacts_ids:
            #     DigitalKeyContact(digital_key=digital_key, contragent_id=_id,
            #                       type=DigitalKeyContact.CONTACT).save()
            return redirect('digital_key:show_by_id', digital_key.id)
    else:
        digital_key_form = DigitalKeyForm(instance=digital_key)
    return render(request, 'digital_key/edit.html', {
        'digitalkey_form': digital_key_form,
        'holders': [],
        'contacts': []
    })


def remove_by_id(request, key_id):
    digital_key = get_object_or_404(DigitalKey, pk=key_id)
    digital_key.delete()
    return redirect('digital_key:all')


def location_detail(request, pk):
    location = get_object_or_404(KeyLocation, pk=pk)
    key_views = [DigitalKeyWrapper(key) for key in location.digitalkey_set.all()]
    return render(request, 'digital_key/location_detail.html', {
        'keylocation': location,
        'key_views': key_views
    })


def location_list(request):
    locations = KeyLocation.objects.all()
    return render(request, 'digital_key/location_list.html', {
        'locations': locations
    })


def system_list(request):
    systems = WorkSystem.objects.all()
    return render(request, 'digital_key/systems_list.html', {
        'systems': systems
    })


def system_detail(request, pk):
    system = get_object_or_404(WorkSystem, pk=pk)
    key_views = [DigitalKeyWrapper(key) for key in system.digitalkey_set.all()]
    return render(request, 'digital_key/system_detail.html', {
        'system': system,
        'key_views': key_views
    })
