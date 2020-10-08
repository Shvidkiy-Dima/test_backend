from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    regex = r'^((\+7|7|8)+([0-9]){10})$'
    message = 'Please enter valid phone number - example +78005553535'

    def __init__(self):
        super().__init__()
