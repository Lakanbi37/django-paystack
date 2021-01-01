from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_paystack.apps.customer.models import Customer
# Create your models here.


class TransferManager(models.Manager):

    def add_transfer(self, data, recipient):
        obj = self.model(**data)
        obj.recipient = recipient
        obj.save()
        return obj

    def update_status(self, code, status, ref):
        return self.filter(transfer_code=code).update(status=status, reference=ref)


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
    transfer_id = models.CharField(max_length=2000, null=True, blank=True)
    transfer_code = models.CharField(max_length=200)
    recipient = models.ForeignKey("Recipient", on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=10, default="NGN", blank=True, null=True)
    source = models.CharField(max_length=150, choices=TRANSFER_CHOICE, default=BALANCE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    reference = models.CharField(max_length=120, null=True, blank=True)
    reason = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = TransferManager()

    def __str__(self):
        return self.transfer_code

    class Meta:
        app_label = "transfers"


class Recipient(models.Model):
    NUBAN = _("nuban")
    RECIPIENT_CHOICES = (
        (NUBAN, _("Nuban")),
    )
    recipient_id = models.CharField(max_length=2000, null=True, blank=True)
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
        app_label = "transfers"


class AccountDetails(models.Model):
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_code = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return self.account_name if self.account_name else str(self.account_number)

    class Meta:
        verbose_name = "Account Details"
        verbose_name_plural = "Account Details"
        app_label = "transfers"
