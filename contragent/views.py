from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from contragent.forms import ContragentForm, ContragentDetailForm, ContragentSearchForm
from digitalkey.support import ContactKeyWrapper
from .models import Contragent, ContactInfo


# Create your views here.

def show_all(request):
    return render(request, 'contragent/list.html', {
        'contragents': Contragent.objects.all()
    })


def show_by_id(request, cid: int):
    contragent = get_object_or_404(Contragent, pk=cid)
    linked_keys_gen = (ContactKeyWrapper(contragent, key) for key in contragent.digitalkey_set.distinct())
    return render(request, 'contragent/detail.html', {
        'contragent': contragent,
        'linked_keys': linked_keys_gen
    })


def show_all_by_type(request, ctype):
    contragents = Contragent.objects.filter(digitalkeycontact__type=ctype[:1]).distinct()
    if not contragents:
        raise Http404('Контакты')
    return render(request, 'contragent/list.html', {
        'contragents': contragents
    })


def edit_by_id(request, cid: int):
    contragent = get_object_or_404(Contragent, pk=cid)
    info_set = contragent.contactinfo_set.all()
    ContactInfoFormSet = modelformset_factory(
        ContactInfo, form=ContragentDetailForm,
        extra=0, can_delete=True)
    if request.method == 'POST':
        contragent_form = ContragentForm(request.POST, instance=contragent)
        info_formset = ContactInfoFormSet(request.POST, queryset=info_set)
        if contragent_form.is_valid() and info_formset.is_valid():
            if contragent_form.has_changed():
                contragent = contragent_form.save()
            if info_formset.has_changed():
                info_formset.save_existing_objects()
                info_formset.saved_forms = []
                for contact_info in info_formset.save_new_objects(commit=False):
                    contact_info.contact = contragent
                    contact_info.save()
            return redirect('contragent:show_by_id', contragent.id)
    else:
        contragent_form = ContragentForm(instance=contragent)
        info_formset = ContactInfoFormSet(queryset=info_set)

    return render(request, 'contragent/edit.html', {
        'contragent_form': contragent_form,
        'info_formset': info_formset
    })


def create(request):
    ContactInfoFormSet = formset_factory(ContragentDetailForm, extra=1, can_delete=True)
    if request.method == 'POST':
        contragent_form = ContragentForm(request.POST)
        info_formset = ContactInfoFormSet(request.POST)
        if contragent_form.is_valid():
            contragent = contragent_form.save()
            if info_formset.is_valid():
                for form in info_formset.forms:
                    contact_info = form.save(commit=False)
                    contact_info.contact = contragent
                    contact_info.save()
            return redirect('contragent:show_by_id', contragent.id)
    else:
        contragent_form = ContragentForm()
        info_formset = ContactInfoFormSet()
    return render(request, 'contragent/edit.html', {
        'contragent_form': contragent_form,
        'info_formset': info_formset
    })


def remove_by_id(request, cid):
    contragent = get_object_or_404(Contragent, pk=cid)
    contragent.delete()
    return redirect('contragent:all')


def show_all_by_name(request):
    if request.method == 'GET':
        form = ContragentSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['search']
            agents = Contragent.objects.filter(name__icontains=name).values('id', 'name')
            response = JsonResponse(list(agents), safe=False)
            return response
    else:
        return JsonResponse({})
