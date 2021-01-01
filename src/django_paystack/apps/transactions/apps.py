from django.utils.translation import gettext_lazy as _
from django_paystack.config import PaystackConfig


class TransactionsConfig(PaystackConfig):
    name = 'django_paystack.apps.transactions'
    label = "transactions"
    verbose_name = _('Transactions')
