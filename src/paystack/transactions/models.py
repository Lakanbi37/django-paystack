from django.db import models
# Create your models here.
from paystack.customer.models import Customer
from paystack.plans.models import Plan


class Transaction(models.Model):
    status = models.CharField(max_length=150, null=True, blank=True)
    reference = models.CharField(max_length=150, blank=True, null=True)
    amount = models.PositiveBigIntegerField(null=True, blank=True)
    gateway_response = models.CharField(max_length=150, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=150, blank=True, null=True)
    currency = models.CharField(max_length=150, default="NGN", blank=True, null=True)
    fees = models.IntegerField(null=True, blank=True)
    fees_split = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    log = models.ForeignKey("transactions.Log", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    source = models.ForeignKey("payment.Source", on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    subaccounts = models.ManyToManyField("payment.SubAccount", through="TransactionSubAccount", through_fields=("transaction", "account"))
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.reference if self.reference is not None else str(self.pk)


class Log(models.Model):
    time_spent = models.IntegerField(blank=True, null=True)
    attempts = models.IntegerField(blank=True, null=True)
    error = models.IntegerField(blank=True, null=True)
    success = models.BooleanField(default=False)
    mobile = models.BooleanField(default=False)
    channel = models.CharField(max_length=100, null=True, blank=True)
    history = models.ManyToManyField("History", through="LogHistory", through_fields=("log", "history"))

    def __str__(self):
        return str(self.pk)


class History(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=150, null=True, blank=True)
    time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class LogHistory(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class TransactionSubAccount(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account = models.ForeignKey("payment.SubAccount", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
