from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django_paystack.apps.customer.API.serializers import CustomerModelSerializer
from django_paystack.apps.payment.api.serializers import SourceModelSerializer
from ..models import Plan, Subscription


class PlanModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = "__all__"


class SubscriptionModelSerializer(serializers.ModelSerializer):
    plan = PlanModelSerializer(read_only=True)
    customer = CustomerModelSerializer(read_only=True)
    source = SourceModelSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"


class PlanSerializer(serializers.Serializer):
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
    name = serializers.CharField(required=True)
    amount = serializers.CharField(required=True)
    interval = serializers.ChoiceField(choices=PLAN_CHOICES, required=True)
    description = serializers.CharField(required=False)
    send_sms = serializers.BooleanField(required=False)
    send_invoices = serializers.BooleanField(required=False)
    currency = serializers.CharField(required=False, default="NGN")


class SubscriptionSerializer(serializers.Serializer):
    customer = serializers.CharField(help_text="Customer code", required=True)
    plan = serializers.CharField(required=True)
    authorization = serializers.CharField(required=False)
    start_date = serializers.DateTimeField(required=False)


class SubscriptionEnableSerializer(serializers.Serializer):
    code = serializers.CharField()
    token = serializers.CharField()

