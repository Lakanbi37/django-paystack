from django.db import models
from django.utils.translation import ugettext_lazy as _
from paystack.customer.models import Customer
# Create your models here.


class Transfer(models.Model):
    BALANCE = _("balance")
    TRANSFER_CHOICE = (
        (BALANCE, _("Balance")),
    )
    PENDING = _("pending")
    OTP = _("otp")
    SUCCESS = _("success")
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (OTP, _("Otp")),
        (SUCCESS, _("Success")),
    )
    transfer_code = models.CharField(max_length=200)
    recipient = models.ForeignKey("Recipient", on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=10, default="NGN", blank=True, null=True)
    source = models.CharField(max_length=150, choices=TRANSFER_CHOICE, default=BALANCE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    reason = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transfer_code


class Recipient(models.Model):
    NUBAN = _("nuban")
    RECIPIENT_CHOICES = (
        (NUBAN, _("Nuban")),
    )
    type = models.CharField(max_length=120, choices=RECIPIENT_CHOICES, default=NUBAN)
    currency = models.CharField(max_length=10, default="NGN", null=True)
    name = models.CharField(max_length=120)
    details = models.ForeignKey("AccountDetails", on_delete=models.CASCADE)
    metadata = models.JSONField(null=True, blank=True)
    recipient_code = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transfer Recipient"
        verbose_name_plural = "Transfer Recipients"


class AccountDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_code = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return self.account_name if self.account_name else str(self.account_number)
