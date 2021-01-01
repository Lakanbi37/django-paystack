from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_paystack.utils.gateway import paystack_gateway
from .serializers import (
    PaymentInitializerSerializer,
    PaymentVerificationSerializer,
    RefundSerializer,
    SubAccountSerializer,
    TransactionSplitSerializer
)
# Create your views here.
from django_paystack.core.loading import get_model

Transaction = get_model("transactions", "Transaction")
Log = get_model("transactions", "Log")
History = get_model("transactions", "History")
Source = get_model("payment", "Source")
Customer = get_model("customer", "Customer")
Plan = get_model("plans", "Plan")
Refund = get_model("payment", "Refund")
SubAccount = get_model("payment", "SubAccount")
SplitAccount = get_model("payment", "SplitAccount")
TransactionSplit = get_model("payment", "TransactionSplit")


class PaymentInitializeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PaymentInitializerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = paystack_gateway.Transaction.initiate(serializer.data)
        return Response(response["data"], status=status.HTTP_202_ACCEPTED)


class PaymentVerificationAPIView(GenericAPIView):
    serializer_class = PaymentVerificationSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        trans_data = self.extract_transaction_data(data)
        plan = self.extract_plan(data)
        log = self.extract_log(data)
        return trans_data, plan, log

    def extract_histories(self, data):
        histories = []
        _data = list(data)
        for history in _data:
            history = History.objects.add_history(history)
            histories.append(history)
        return histories

    def extract_plan(self, data):
        plan_data = dict(**data["plan"])
        if plan_data.__len__() > 0:
            return Plan.objects.new_plan(data=plan_data)
        return None

    def extract_log(self, data):
        log_data = dict(time_spent=data["log"]["time_spent"],
                        attempts=data["log"]["attempts"],
                        errors=data["log"]["errors"],
                        success=data["log"]["success"]
                        )
        log = Log.objects.create(**log_data)
        histories = self.extract_histories(data["log"]["history"])
        for history in histories:
            log.history.add(history)
        log.save()
        return log

    def extract_transaction_data(self, data):
        return dict(amount=data["amount"],
                    reference=data["reference"],
                    status=data["status"],
                    gateway_response=data["gateway_response"],
                    channel=data["channel"],
                    currency=data["currency"],
                    metadata=data["metadata"],
                    requested_amount=data["requested_amount"],
                    fees=data["fees"],
                    fees_split=data["fees_split"],
                    transaction_date=data["transaction_date"],
                    created_at=data["createdAt"],
                    paid_at=data["paidAt"],
                    trans_id=data["id"],
                    )

    def create_transaction(self, data):
        trans_data, plan, log = self.extract(data)
        transaction = Transaction.objects.add_transaction(
            request=self.request,
            data=trans_data,
            log=log,
            plan=plan
        )
        return transaction

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        reference = ser.data["reference"]
        response = paystack_gateway.Transaction.verify(reference)
        self.create_transaction(response["data"])
        return Response(response["data"], status=status.HTTP_200_OK)


class RefundAPIView(GenericAPIView):
    serializer_class = RefundSerializer
    permission_classes = [AllowAny]

    def extract(self, _data):
        transaction = Transaction.objects.get(trans_id=_data["transaction"])
        data = dict(
            amount=_data["amount"],
            deducted_amount=_data["deducted_amount"],
            currency=_data["currency"],
            channel=_data["channel"],
            status=_data["status"],
            refunded_by=_data["refunded_by"],
            refunded_at=_data["refunded_at"],
            expected_at=_data["expected_at"],
            refund_id=_data["id"],
        )
        return transaction, data

    def record_refund(self, data):
        transaction, _data = self.extract(data)
        return Refund.objects.issue_refund(transaction=Transaction, data=_data)

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        refund = paystack_gateway.Refunds.refund(ser.data)
        self.record_refund(refund["data"])
        return Response(refund["data"], status=status.HTTP_202_ACCEPTED)


class SubAccountCreateAPIView(GenericAPIView):
    serializer_class = SubAccountSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        return dict(
            subaccount_code=data["subaccount_code"],
            subaccount_id=data["id"],
            business_name=data["business_name"],
            description=data["description"],
            primary_contact_name=data["primary_contact_name"],
            primary_contact_email=data["primary_contact_email"],
            primary_contact_phone=data["primary_contact_phone"],
            settlement_bank=data["settlement_bank"],
            account_number=data["account_number"],
            percentage_charge=data["percentage_charge"]
        )

    def record_entry(self, data):
        _data = self.extract(data)
        return SubAccount.objects.add_account(_data)

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        response = paystack_gateway.Subaccount.create(ser.data)
        self.record_entry(response["data"])
        return Response(response["data"], status=status.HTTP_201_CREATED)


class TransactionSplitCreateAPIView(GenericAPIView):
    serializer_class = TransactionSplitSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        subaccounts = self.extract_accounts(data["subaccounts"])
        split_data = dict(
            split_id=data["id"],
            name=data["name"],
            type=data["type"],
            currency=data["currency"],
            split_code=data["split_code"],
            bearer_type=data["bearer_type"],
            bearer_subaccount=data["bearer_subaccount"]
        )
        return split_data, subaccounts

    def extract_accounts(self, data):
        accts = list(data)
        accounts = []
        for acct in accts:
            sub = SubAccount.objects.get(subaccount_code=acct["subaccount"]["subaccount_code"])
            account = SplitAccount.objects.add_new(account=sub, share=acct["share"])
            accounts.append(account)
        return accounts

    def record_entry(self, data):
        split_data, accounts = self.extract(data)
        split = TransactionSplit.objects.add_split(data=split_data, accounts=accounts)
        return split

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = paystack_gateway.Split.create(serializer.data)
        self.record_entry(response["data"])
        return Response(response, status=status.HTTP_201_CREATED)
