from django.utils.translation import gettext_lazy as _
from django_paystack.config import PaystackConfig


class BanksConfig(PaystackConfig):
    label = "banks"
    name = 'django_paystack.apps.banks'
    verbose_name = _('Bank')
