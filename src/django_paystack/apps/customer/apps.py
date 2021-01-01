from django.utils.translation import gettext_lazy as _
from django_paystack.config import PaystackConfig


class CustomerConfig(PaystackConfig):
    label = "customer"
    name = 'django_paystack.apps.customer'
    verbose_name = _('Customer')

    def ready(self):
        from . import recievers
        super().ready()
