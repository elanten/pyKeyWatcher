from django import forms

from employee.models import ContactType, Employee, ContactInfo

# detail_type_list = list((detail.id, detail.name) for detail in ContactType.objects.all())


class EmployeeForm(forms.ModelForm):
    def get_id(self):
        if self.instance:
            return self.instance.id

    class Meta:
        model = Employee
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class EmployeeDetailForm(forms.ModelForm):
    error_css_class = 'bg-danger'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(EmployeeDetailForm, self).__init__(*args, **kwargs)
        self.fields['contact_type'].empty_label = None
        # self.auto_id = False

    def has_error_class(self):
        if any(self.errors):
            return self.error_css_class
        else:
            return ''

    class Meta:
        model = ContactInfo
        fields = ['type', 'value']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control select-noarrow'}),
            'value': forms.TextInput(attrs={'class': 'form-control'})
        }


class ContragentSearchForm(forms.Form):
    search = forms.CharField(min_length=3)
