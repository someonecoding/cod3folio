from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

def email_user_exists(email):
    try:
        user = CustomUser.objects.get(email=email)
    except:
        raise ValidationError(_(
            'email does not exist'
        ))
    if user.email_verified:
        raise ValidationError(
            _('Account already activated')
        )