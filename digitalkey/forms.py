from django import forms
from django.forms import Textarea
from django.forms.widgets import TextInput, Select
from digitalkey.models import DigitalKey


class DigitalKeyForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=200, label="Наименование")
    serial = forms.CharField(min_length=3, max_length=200)
    description = forms.CharField(initial="", widget=Textarea(attrs={'class': 'form-control', 'rows': 4}))
    expire = forms.DateField(input_formats=['%Y-%m-%d'], widget=TextInput)

    def get_id(self):
        if self.instance:
            return self.instance.id

    class Meta:
        model = DigitalKey
        fields = ['name', 'serial', 'description', "date_end", 'key_type', 'key_allocation']

