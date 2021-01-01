from django.db import models
from django_paystack.apps.customer.models import Customer
# Create your models here.


class SourceManager(models.Manager):

    def add_source(self, customer, data):
        obj = self.model(**data)
        obj.customer = customer
        obj.save()
        return obj


class Source(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="authorizations")
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

    objects = SourceManager()

    def __str__(self):
        return


class SplitManager(models.Manager):

    def add_split(self, data, accounts=None):
        obj = self.model(**data)
        if accounts is None:
            accounts = []
        for account in accounts:
            obj.subaccounts.add(account)
        obj.save()
        return obj


class TransactionSplit(models.Model):
    split_id = models.CharField(max_length=2000, null=True, blank=True)
    name = models.CharField(max_length=120)
    split_code = models.CharField(max_length=200)
    type = models.CharField(max_length=150, blank=True, null=True)
    currency = models.CharField(default="NGN", max_length=10, null=True, blank=True)
    bearer_type = models.CharField(null=True, blank=True, max_length=100)
    bearer_subaccount = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subaccounts = models.ManyToManyField("SplitAccount", blank=True)

    objects = SplitManager()

    def __str__(self):
        return str(self.split_code)

    class Meta:
        app_label = "payment"


class SubAccountManager(models.Manager):

    def add_account(self, data):
        return self.create(**data)


class SubAccount(models.Model):
    subaccount_id = models.CharField(max_length=2000, null=True, blank=True)
    subaccount_code = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    primary_contact_name = models.CharField(max_length=200, null=True, blank=True)
    primary_contact_email = models.CharField(max_length=200, null=True, blank=True)
    primary_contact_phone = models.CharField(max_length=13, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    settlement_bank = models.CharField(max_length=200)
    account_number = models.IntegerField()
    percentage_charge = models.PositiveBigIntegerField(help_text="Percentage Share")

    objects = SubAccountManager()

    def __str__(self):
        return self.subaccount_code


class RefundManager(models.Manager):

    def issue_refund(self, transaction, data):
        obj = self.model(**data)
        obj.transaction = transaction
        obj.save()
        return obj


class Refund(models.Model):
    refund_id = models.CharField(max_length=2000, null=True, blank=True)
    transaction = models.ForeignKey("transactions.Transaction", on_delete=models.CASCADE)
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

    objects = RefundManager()

    def __str__(self):
        return str(self.transaction.reference)


class SplitAccountManager(models.Manager):

    def add_new(self, account, share):
        return self.create(account=account, share=share)


class SplitAccount(models.Model):
    account = models.ForeignKey(SubAccount, on_delete=models.CASCADE)
    share = models.PositiveBigIntegerField()

    objects = SplitAccountManager()

    def __str__(self):
        return str(self.account)