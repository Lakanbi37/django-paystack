# flake8: noqa, because URL syntax is more readable with long lines
from django.apps import apps
from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from django_paystack.utils.config import PaystackConfig
from django_paystack.core.loading import get_class


class DjangoPaystack(PaystackConfig):
    name = 'django_paystack'

    def ready(self):
        self.charge_app = apps.get_app_config('charge')
        self.payment_app = apps.get_app_config("payment")
        self.plans_app = apps.get_app_config("plans")
        self.transfers_app = apps.get_app_config("transfers")

    def get_urls(self):
        urls = [
            path("charge/", self.charge_app.urls),
            path("payments/", self.payment_app.urls),
            path("plans/", self.plans_app.urls),
            path("transfers/", self.transfers_app.urls),
        ]
        return urls
