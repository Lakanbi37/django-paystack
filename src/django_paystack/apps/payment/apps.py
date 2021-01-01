from django.utils.translation import gettext_lazy as _
from django.urls import path
from django_paystack.config import PaystackConfig
from django_paystack.core.loading import get_class


class PaymentConfig(PaystackConfig):
    label = "payment"
    name = 'django_paystack.apps.payment'
    verbose_name = _('Payment')

    def ready(self):
        self.payment_initialize_view = get_class("payment.api.views", "PaymentInitializeAPIView")
        self.payment_verify_view = get_class("payment.api.views", "PaymentVerificationAPIView")

    def get_urls(self):
        urls = [
            path('initialize/', self.payment_initialize_view.as_view()),
            path('verify/', self.payment_verify_view.as_view()),
        ]
        return self.post_process_urls(urls)


