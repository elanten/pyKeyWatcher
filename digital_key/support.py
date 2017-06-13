from .models import DigitalKey
from django.utils import timezone


class DigitalKeyWrapper:
    def __init__(self, digitalkey: DigitalKey, default_style='default'):
        self.key = digitalkey
        self.style = default_style
        self.days_left = 0
        self.is_copy = digitalkey.is_copy()
        self.copy_type = 'Копия' if self.is_copy else 'Оригинал'
        self.copies_count = digitalkey.get_copies().count()
        if digitalkey.date_expire:
            timedelta = digitalkey.date_expire - timezone.now().date()
            self.days_left = timedelta.days
            if self.days_left < 30:
                self.style = 'danger'
            elif self.days_left < 60:
                self.style = 'warning'

    def name(self):
        return self.__key.name

    def serial(self):
        return self.__key.serial

    def description(self):
        return self.__key.description

    def date_begin(self):
        return self.__key.date_begin if not self.is_copy else self.__key.copy_of.date_begin

    def date_expire(self):
        return self.__key.date_expire if not self.is_copy else self.__key.copy_of.date_expire


class EmployeeKeyWrapper(DigitalKeyWrapper):
    def __init__(self, contragent, digitalkey):
        super().__init__(digitalkey, default_style='success')
        self.is_holded = digitalkey.digitalkeycontact_set.filter(contragent=contragent, type='h').count() > 0
        self.is_contacted = digitalkey.digitalkeycontact_set.filter(contragent=contragent, type='c').count() > 0
