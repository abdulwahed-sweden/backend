from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class SwedishPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 10:
            raise ValidationError(
                _("Lösenordet måste vara minst 10 tecken långt."),
                code='password_too_short',
            )