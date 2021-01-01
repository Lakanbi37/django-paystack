from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django_paystack.core.loading import get_model
from django_paystack.utils.gateway import paystack_gateway
from .serializers import PlanSerializer, SubscriptionSerializer, SubscriptionEnableSerializer

Plan = get_model("plans", "Plan")
Customer = get_model("customer", "Customer")
Source = get_model("payment", "Source")
Subscription = get_model("plans", "Subscription")


class PlanCreateAPIView(GenericAPIView):
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        extract = dict(
            plan_id=data["id"],
            name=data["name"],
            plan_code=data["plan_code"],
            amount=data["amount"],
            send_invoices=data["send_invoices"],
            send_sms=data["send_sms"],
            hosted_page=data["hosted_page"],
            interval=data["interval"],
            currency=data["currency"]
        )
        return extract

    def record_entry(self, data):
        plan_data = self.extract(data)
        return Plan.objects.new_plan(data=plan_data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = paystack_gateway.Plans.create(serializer.data)
        data = response["data"]
        self.record_entry(data)
        return Response(data, status=status.HTTP_201_CREATED)


class SubscribeAPIView(GenericAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

    def extract(self, data):
        customer = Customer.objects.get(user=self.request.user, customer_id=data["customer"])
        plan = Plan.objects.get(plan_id=data["plan"])
        source = Source.objects.get_or_create(**data["authorization"])[0]
        _data = dict(
            subscription_code=data["subscription_code"],
            email_token=data["email_token"],
            subscription_id=data["id"],
            amount=data["amount"],
            start=data["start"],
            status=data["status"],
        )
        return customer, plan, source, _data

    def record_entry(self, data):
        customer, plan, source, _data = self.extract(data)
        return Subscription.objects.add_subscription(
            customer=customer,
            source=source,
            plan=plan,
            data=_data
        )

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        subscription = paystack_gateway.Subscriptions.create(ser.data)
        data = subscription["data"]
        self.record_entry(data)
        return Response(data, status=status.HTTP_201_CREATED)


class EnableSubscriptionAPIView(GenericAPIView):
    serializer_class = SubscriptionEnableSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        enabled = paystack_gateway.Subscriptions.activate(ser.data)
        return Response(enabled, status=status.HTTP_202_ACCEPTED)


class DisableSubscriptionAPIView(GenericAPIView):
    serializer_class = SubscriptionEnableSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        disabled = paystack_gateway.Subscriptions.deactivate(serializer.data)
        return Response(disabled, status=status.HTTP_202_ACCEPTED)
