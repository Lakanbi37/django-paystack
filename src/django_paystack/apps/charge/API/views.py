from rest_framework import status
from rest_framework.response import Response
from django_paystack.apps.payment.api.views import PaymentVerificationAPIView, paystack_gateway
from .serializers import BankChargeSerializer


class ChargeBankAPIView(PaymentVerificationAPIView):
    serializer_class = BankChargeSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        response = paystack_gateway.Charge.bank_charge(ser.data)
        self.create_transaction(response["data"])
        return Response(response, status=status.HTTP_202_ACCEPTED)
