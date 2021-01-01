from rest_framework import serializers
from django_paystack.apps.banks.API.serializers import BankChargeSerializer


class BankChargeSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    bank = BankChargeSerializer(required=True)
    metadata = serializers.JSONField(required=False)
    authorization_code = serializers.CharField(required=False)