from rest_framework import serializers
from ..models import Bank


class BankChargeSerializer(serializers.Serializer):
    code = serializers.CharField()
    account_number = serializers.CharField()


class BankModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = "__all__"