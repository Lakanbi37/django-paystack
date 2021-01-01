from django.urls import path
from django.utils.translation import gettext_lazy as _
from django_paystack.config import PaystackConfig
from django_paystack.core.loading import get_class


class ChargeConfig(PaystackConfig):
    name = 'django_paystack.apps.charge'
    label = 'charge'
    verbose_name = _('Charge')

    def ready(self):
        self.charge_bank_api = get_class("charge.API.views", "ChargeBankAPIView")

    def get_urls(self):
        urls = [
            path('bank/', self.charge_bank_api.as_view()),
        ]
        return self.post_process_urls(urls)
