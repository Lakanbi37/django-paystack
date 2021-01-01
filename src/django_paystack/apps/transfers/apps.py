from django.utils.translation import gettext_lazy as _
from django.urls import path
from django_paystack.core.loading import get_class
from django_paystack.config import PaystackConfig


class TransfersConfig(PaystackConfig):
    name = 'django_paystack.apps.transfers'
    label = "transfers"
    verbose_name = _('Transfers')

    def ready(self):
        self.transfer_api = get_class("transfers.API.views", "TransferAPIView")
        self.beneficiary_add_api = get_class("transfers.API.views", "TransferRecipientCreateAPIView")
        self.finalize_transfer_api = get_class("transfers.API.views", "TransferFinalizeAPIView")
        self.bulk_transfer_api = get_class("transfers.API.views", "BulkTransferAPIView")
        self.transfer_verify_api = get_class("transfers.API.views", "TransferVerifyAPIView")

    def get_urls(self):
        urls = [
            path('bulk/', self.bulk_transfer_api.as_view()),
            path('finalize/', self.finalize_transfer_api.as_view()),
            path('initiate/', self.transfer_api.as_view()),
            path('verify/', self.transfer_verify_api.as_view()),
            path('beneficiary/add/', self.beneficiary_add_api.as_view()),
        ]
        return self.post_process_urls(urls)
