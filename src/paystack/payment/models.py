from django.db import models
from paystack.customer.models import Customer
from paystack.transactions.models import Transaction
# Create your models here.


class Source(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    authorization_code = models.CharField(max_length=200, blank=True, null=True)
    card_type = models.CharField(max_length=100, blank=True, null=True)
    last4 = models.CharField(max_length=4, null=True)
    exp_month = models.CharField(max_length=2, null=True)
    exp_year = models.CharField(max_length=4, null=True)
    bin = models.CharField(max_length=10, null=True)
    bank = models.CharField(max_length=50, null=True)
    brand = models.CharField(max_length=10, null=True, blank=True)
    channel = models.CharField(max_length=30, null=True, blank=True)
    signature = models.CharField(max_length=200, null=True, blank=True)
    reusable = models.BooleanField(default=True)
    country_code = models.CharField(max_length=10, null=True)
    account_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return


class TransactionSplit(models.Model):
    name = models.CharField(max_length=120)
    split_code = models.CharField(max_length=200)
    integration = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    currency = models.CharField(default="NGN", max_length=10, null=True, blank=True)
    bearer_type = models.CharField(null=True, blank=True, max_length=100)
    bearer_subaccount = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subaccounts = models.ManyToManyField("SubAccount", through="SplitSubAccount", through_fields=("split", "account"))

    def __str__(self):
        return str(self.split_code)


class SubAccount(models.Model):
    subaccount_code = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    primary_contact_name = models.CharField(max_length=200, null=True, blank=True)
    primary_contact_email = models.CharField(max_length=200, null=True, blank=True)
    primary_contact_phone = models.CharField(max_length=13, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    settlement_bank = models.CharField(max_length=200)
    account_number = models.IntegerField()
    share = models.PositiveBigIntegerField(help_text="Percentage Share")

    def __str__(self):
        return self.subaccount_code


class Refund(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    deducted_amount = models.PositiveBigIntegerField()
    fully_deducted = models.BooleanField(default=False)
    currency = models.CharField(max_length=10, default="NGN", blank=True, null=True)
    channel = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=100)
    refunded_by = models.EmailField()
    refunded_at = models.DateTimeField()
    expected_at = models.DateTimeField()
    customer_note = models.TextField(null=True, blank=True)
    merchant_note = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.transaction.reference)


class SplitSubAccount(models.Model):
    split = models.ForeignKey(TransactionSplit, on_delete=models.CASCADE)
    account = models.ForeignKey(SubAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)