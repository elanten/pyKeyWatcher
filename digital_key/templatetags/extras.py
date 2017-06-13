from django.forms.boundfield import BoundField
from django.template.defaultfilters import register


@register.filter(is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.filter(is_safe=True)
def field_with_classes(field: BoundField, arg) -> BoundField:
    field.field.widget.attrs['class'] = arg
    return field
