from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
    TransferRecipientSerializer,
    TransferSerializer,
    TransferFinalizeSerializer,
    BulkTransferSerializer,
    TransferVerifySerializer
)
from django_paystack.utils.gateway import paystack_gateway
from django_paystack.core.loading import get_model

AccountDetails = get_model("transfers", "AccountDetails")
Recipient = get_model("transfers", "Recipient")
Transfer = get_model("transfers", "Transfer")


class TransferRecipientCreateAPIView(GenericAPIView):
    serializer_class = TransferRecipientSerializer
    permission_classes = [AllowAny]

    def extract_data(self, data):
        r_data = dict(name=data["name"],
                      type=data["type"],
                      currency=data["currency"],
                      recipient_code=data["recipient_code"],
                      metadata=data["recipient_code"],
                      recipient_id=data["id"],
                      created_at=data["createdAt"],
                      updated_at=data["updatedAt"]
                      )
        account_data = dict(**data["details"])
        return r_data, account_data

    def record_beneficiary(self, data):
        r_data, acct_data = self.extract_data(data)
        account_details = AccountDetails.objects.create(**acct_data)
        recipient = Recipient(**r_data)
        recipient.details = account_details
        recipient.save()
        return recipient

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = paystack_gateway.Transfers.add_beneficiary(serializer.data)
        self.record_beneficiary(response["data"])
        return Response(response["data"], status=status.HTTP_201_CREATED)


class TransferAPIView(GenericAPIView):
    serializer_class = TransferSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        extract = dict(
            amount=data["amount"],
            source=data["source"],
            status=data["status"],
            transfer_code=data["transfer_code"],
            currency=data["currency"],
            reason=data["reason"],
            transfer_id=data["id"],
        )
        recipient = Recipient.objects.get(recipient_id=data["recipient"])
        return extract, recipient

    def record_transfer(self, data):
        response, recipient = self.extract(data)
        trans_obj = Transfer.objects.add_transfer(data=response, recipient=recipient)
        return trans_obj

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        transfer_response = paystack_gateway.Transfers.initiate(ser.data)
        self.record_transfer(transfer_response["data"])
        return Response(transfer_response["data"], status=status.HTTP_201_CREATED)


class TransferFinalizeAPIView(GenericAPIView):
    serializer_class = TransferFinalizeSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        code = data["transfer_code"]
        _status = data["status"]
        reference = data["reference"]
        return code, _status, reference

    def update(self, data):
        code, _status, reference = self.extract(data)
        return Transfer.objects.update_status(code=code, status=_status, ref=reference)

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        response = paystack_gateway.Transfers.finalize(ser.data)
        self.update(response["data"])
        return Response(response["data"], status=status.HTTP_200_OK)


class BulkTransferAPIView(GenericAPIView):
    serializer_class = BulkTransferSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        extract = list(data)
        return extract

    def record(self, item):
        recipient = Recipient.objects.get(recipient_code=item["recipient"])
        data = dict(amount=item["amount"], transfer_code=item["transfer_code"], currency=item["currency"])
        transfer = Transfer.objects.add_transfer(data=data, recipient=recipient)
        return transfer

    def record_transfers(self, data):
        extracted = self.extract(data)
        for extract in extracted:
            self.record(extract)

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        response = paystack_gateway.Transfers.initiate_bulk(ser.data)
        self.record_transfers(response["data"])
        return Response(response["data"], status=status.HTTP_201_CREATED)


class TransferVerifyAPIView(GenericAPIView):
    serializer_class = TransferVerifySerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        code = data["transfer_code"]
        _status = data["status"]
        reference = data["reference"]
        return code, _status, reference

    def update(self, data):
        code, _status, ref = self.extract(data)
        transfer = Transfer.objects.update_status(code=code, status=_status, ref=ref)
        return transfer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ref = ser.data["reference"]
        response = paystack_gateway.Transfers.verify(reference=ref)
        self.update(response["data"])
        return Response(response["data"], status=status.HTTP_200_OK)