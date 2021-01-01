from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_paystack.apps.customer.models import Customer


# Create your models here.


class PlanManager(models.Manager):

    def new_plan(self, data):
        return self.create(**data)


class Plan(models.Model):
    WEEKLY = _("weekly")
    MONTHLY = _("monthly")
    ANNUALLY = _("annually")
    DAILY = _("daily")
    HOURLY = _("hourly")
    BIANNUALLY = _("biannually")
    PLAN_CHOICES = (
        (HOURLY, _("Hourly")),
        (DAILY, _("Daily")),
        (WEEKLY, _("Weekly")),
        (MONTHLY, _("Monthly")),
        (ANNUALLY, _("Annually")),
        (BIANNUALLY, _("Biannually")),
    )
    plan_id = models.CharField(max_length=2000, null=True, blank=True)
    name = models.CharField(max_length=120)
    plan_code = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    interval = models.CharField(max_length=120, choices=PLAN_CHOICES, default=MONTHLY)
    amount = models.PositiveBigIntegerField()
    send_invoices = models.BooleanField(default=True)
    hosted_page = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=True)
    hosted_page_url = models.CharField(max_length=120, null=True, blank=True)
    currency = models.CharField(max_length=10, default="NGN", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PlanManager()

    def __str__(self):
        return self.plan_code


class SubscriptionManager(models.Manager):

    def add_subscription(self, plan, source, customer, data):
        obj = self.model(**data)
        obj.plan = plan
        obj.source = source
        obj.customer = customer
        obj.save()
        return obj


class Subscription(models.Model):
    subscription_id = models.CharField(max_length=2000, null=True, blank=True)
    subscription_code = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    source = models.ForeignKey("payment.Source", on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    amount = models.PositiveBigIntegerField(null=True, blank=True)
    start = models.IntegerField()
    email_token = models.CharField(max_length=120)
    next_payment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SubscriptionManager()

    def __str__(self):
        return self.subscription_code
