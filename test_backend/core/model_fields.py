from django.db.models import CharField
from .validators import PhoneNumberValidator


class PhoneNumberField(CharField):
    max_phone_number_length = 12

    def __init__(self, **kwargs):
        kwargs['max_length'] = self.max_phone_number_length
        super().__init__(**kwargs)
        self.validators.append(PhoneNumberValidator())
