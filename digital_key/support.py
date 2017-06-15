from .models import DigitalKey
from django.utils import timezone


class DigitalKeyWrapper:
    def __init__(self, digitalkey: DigitalKey, default_style='default'):
        self.key = digitalkey
        self.default_style = default_style
        self.is_copy = digitalkey.is_copy()
        self.days_left = digitalkey.days_left()
        self.days_before_renewal = self.days_left - digitalkey.renewal_time

    def copies_count(self):
        return self.key.get_copies().count()

    def get_label_class(self):
        if not self.key.date_expire:
            return self.default_style
        delta = self.days_before_renewal
        if delta < 14:
            return 'danger'
        elif delta < 30:
            return 'warning'
        else:
            return 'success'


class EmployeeKeyWrapper(DigitalKeyWrapper):
    def __init__(self, contragent, digitalkey):
        super().__init__(digitalkey, default_style='success')
        self.is_holded = digitalkey.digitalkeycontact_set.filter(contragent=contragent, type='h').count() > 0
        self.is_contacted = digitalkey.digitalkeycontact_set.filter(contragent=contragent, type='c').count() > 0
