from django import forms

from contragent.models import ContactType, Contragent, ContactInfo

detail_type_list = list((detail.id, detail.name) for detail in ContactType.objects.all())


class ContragentForm(forms.ModelForm):
    def get_id(self):
        if self.instance:
            return self.instance.id

    class Meta:
        model = Contragent
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class ContragentDetailForm(forms.ModelForm):
    error_css_class = 'bg-danger'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(ContragentDetailForm, self).__init__(*args, **kwargs)
        self.fields['contact_type'].empty_label = None
        # self.auto_id = False

    def clean(self):
        cleaned_data = super(ContragentDetailForm, self).clean()

    def has_error_class(self):
        if any(self.errors):
            return self.error_css_class
        else:
            return ''

    class Meta:
        model = ContactInfo
        fields = ['contact_type', 'value']
        widgets = {
            'contact_type': forms.Select(attrs={'class': 'form-control select-noarrow'}),
            'value': forms.TextInput(attrs={'class': 'form-control'})
        }


class ContragentSearchForm(forms.Form):
    search = forms.CharField(min_length=3)
