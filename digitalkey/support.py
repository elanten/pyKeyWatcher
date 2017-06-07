from .models import DigitalKey
from django.utils import timezone


class DigitalKeyWrapper:
    def __init__(self, digitalkey: DigitalKey, default_style='default'):
        timedelta = digitalkey.expire - timezone.now().date()
        days_left = timedelta.days
        style = default_style
        if days_left < 30:
            style = 'danger'
        elif days_left < 60:
            style = 'warning'

        self.key = digitalkey
        self.style = style
        self.days_left = days_left


class ContactKeyWrapper(DigitalKeyWrapper):
    def __init__(self, contragent, digitalkey):
        super().__init__(digitalkey, default_style='success')
        self.is_holded = digitalkey.digitalkeycontact_set.filter(contragent=contragent, type='h').count() > 0
        self.is_contacted = digitalkey.digitalkeycontact_set.filter(contragent=contragent, type='c').count() > 0
