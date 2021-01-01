from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django_paystack.apps.transactions.models import Transaction, Log, History
from django_paystack.apps.customer.API.serializers import CustomerModelSerializer
from ..models import Source


class SourceModelSerializer(serializers.ModelSerializer):
    customer = CustomerModelSerializer()

    class Meta:
        model = Source
        fields = "__all__"


class PaymentInitializerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    amount = serializers.IntegerField(required=True)
    currency = serializers.CharField(default="NGN", required=False)
    plan = serializers.CharField(help_text="Plan code", required=False)
    metadata = serializers.JSONField(required=False)
    split_code = serializers.CharField(required=False)
    subaccount = serializers.CharField(required=False)
    transaction_charge = serializers.IntegerField(required=False)
    bearer = serializers.CharField(default="account", required=False)
    callback_url = serializers.CharField(required=False)


class PaymentVerificationSerializer(serializers.Serializer):
    reference = serializers.CharField(required=True)


class SubAccountSerializer(serializers.Serializer):
    business_name = serializers.CharField(help_text="Name of the business", required=True)
    settlement_bank = serializers.CharField(help_text="Bank code for the bank", required=True)
    account_number = serializers.CharField(help_text="Bank account number", required=True)
    percentage_charge = serializers.FloatField(help_text="The default percentage charged when receiving on behalf of "
                                                         "this subaccount", required=True)
    description = serializers.CharField(required=False, help_text="Description for this subaccount")
    primary_contact_email = serializers.EmailField(required=False, help_text="A contact email for this subaccount")
    primary_contact_name = serializers.CharField(required=False, help_text="A name for the contact person for this "
                                                                           "subaccount")
    primary_contact_phone = serializers.CharField(required=False,
                                                  help_text="A phone number to call for this subaccount")
    metadata = serializers.JSONField(required=False)


class TransactionSpliSubAccountSerializer(serializers.Serializer):
    subaccount = serializers.CharField(required=True)
    share = serializers.IntegerField(required=True)


class TransactionSplitSerializer(serializers.Serializer):
    FLAT = _("flat")
    PERCENTAGE = _("percentage")
    TYPE_CHOICES = (
        (FLAT, _("Flat")),
        (PERCENTAGE, _("Percentage")),
    )
    SUBACCOUNT = _("subaccount")
    ACCOUNT = _("account")
    ALL = _("all")
    ALL_PROPORTIONAL = _("all-proportional")
    BEARER_CHOICES = (
        (SUBACCOUNT, _("Subaccount")),
        (ACCOUNT, _("Account")),
        (ALL, _("All")),
        (ALL_PROPORTIONAL, _("All Proportional")),
    )
    name = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=TYPE_CHOICES, default=PERCENTAGE)
    subaccounts = TransactionSpliSubAccountSerializer(many=True, required=True)
    currency = serializers.CharField(required=False, default="NGN")
    bearer_type = serializers.ChoiceField(choices=BEARER_CHOICES, default=SUBACCOUNT)
    bearer_subaccount = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs["bearer_type"] == "subaccount" and attrs["bearer_subaccount"] == "":
            raise serializers.ValidationError(detail="Bearer sub account code required for 'Subaccount' bearer type")
        return attrs


class RefundSerializer(serializers.Serializer):
    transaction = serializers.CharField(required=True, help_text="transaction id or reference")
    amount = serializers.IntegerField(required=False)
    currency = serializers.CharField(required=False, default="NGN")
    customer_note = serializers.CharField(required=False)
    merchant_note = serializers.CharField(required=False)

    def validate(self, attrs):
        transaction_id = attrs["transaction"]
        amount = attrs.get("amount", None)
        try:
            trans = Transaction.objects.get(id=transaction_id)
        except Exception as e:
            trans = Transaction.objects.get(reference=transaction_id)
        if amount is not None:
            if amount > trans.amount:
                raise serializers.ValidationError(f"Invalid amount. only {trans.amount} is refundable")
        return attrs


class LogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = "__all___"


class TransactionModelSerializer(serializers.ModelSerializer):
    source = SourceModelSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"