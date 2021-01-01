from django.db import models
# Create your models here.
from django_paystack.apps.customer.models import Customer
from django_paystack.apps.plans.models import Plan
from django_paystack.apps.payment.models import Source


class TransactionManager(models.Manager):

    def add_transaction(self, request, data, log=None, plan=None):
        customer = Customer.objects.get_or_create(user=request.user, customer_code=data["customer"]["customer_code"])
        try:
            source = Source.objects.get(authorization_code=data["authorization"]["authorization_code"])
        except Exception as e:
            source = Source.objects.add_source(customer, data["authorization"])
        obj = self.model(**data)
        obj.source = source
        obj.customer = customer
        if log is not None:
            obj.log = log
        if plan is not None:
            obj.plan = plan
        obj.save()
        return obj


class Transaction(models.Model):
    trans_id = models.CharField(max_length=2000, null=True, blank=True)
    status = models.CharField(max_length=150, null=True, blank=True)
    reference = models.CharField(max_length=150, blank=True, null=True)
    amount = models.PositiveBigIntegerField(null=True, blank=True)
    gateway_response = models.CharField(max_length=150, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=150, blank=True, null=True)
    currency = models.CharField(max_length=150, default="NGN", blank=True, null=True)
    fees = models.PositiveBigIntegerField(null=True, blank=True)
    fees_split = models.PositiveBigIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    log = models.ForeignKey("Log", on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey("payment.Source", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    subaccounts = models.ManyToManyField("payment.SubAccount", blank=True)
    requested_amount = models.PositiveBigIntegerField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    objects = TransactionManager()

    def __str__(self):
        return self.reference if self.reference is not None else str(self.pk)


class LogManager(models.Manager):

    def add_log_entry(self, data):
        return self.create(**data)


class Log(models.Model):
    time_spent = models.IntegerField(blank=True, null=True)
    attempts = models.IntegerField(blank=True, null=True)
    errors = models.IntegerField(blank=True, null=True)
    success = models.BooleanField(default=False)
    mobile = models.BooleanField(default=False)
    channel = models.CharField(max_length=100, null=True, blank=True)
    history = models.ManyToManyField("History")
    objects = LogManager()

    def __str__(self):
        return str(self.pk)


class HistoryManager(models.Manager):

    def add_history(self, data):
        return self.create(**data)


class History(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=150, null=True, blank=True)
    time = models.IntegerField(blank=True, null=True)

    objects = HistoryManager()

    def __str__(self):
        return str(self.pk)
