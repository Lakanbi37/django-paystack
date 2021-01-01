from rest_framework import serializers
from ..models import Transfer, Recipient, AccountDetails


class AccountDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountDetails
        fields = "__all__"


class RecipientSerializer(serializers.ModelSerializer):
    details = AccountDetailsSerializer(read_only=True)

    class Meta:
        model = Recipient
        fields = "__all__"


class TransferModelSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer(read_only=True)

    class Meta:
        model = Transfer
        fields = "__all__"


class TransferSerializer(serializers.Serializer):
    source = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)
    recipient = serializers.CharField(required=True)
    reason = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)


class TransferFinalizeSerializer(serializers.Serializer):
    transfer_code = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)


class TransferItemSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    recipient = serializers.CharField(required=True)
    reference = serializers.CharField(required=False)


class BulkTransferSerializer(serializers.Serializer):
    source = serializers.CharField(required=True)
    transfers = TransferItemSerializer(many=True)
    currency = serializers.CharField(required=False)


class TransferRecipientSerializer(serializers.Serializer):
    type = serializers.Serializer(required=True)
    name = serializers.Serializer(required=True)
    account_number = serializers.CharField(required=True)
    bank_code = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    authorization_code = serializers.CharField(required=False)
    metadata = serializers.JSONField(required=False)


class BulkTranferRecipientSerializer(serializers.Serializer):
    batch = TransferRecipientSerializer(many=True, required=True)


class TransferVerifySerializer(serializers.Serializer):
    reference = serializers.CharField()