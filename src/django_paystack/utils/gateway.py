import paystack
from django.conf import settings

SECRET_KEY = getattr(settings, "PAYSTACK_SECRET_KEY", "")
PUBLIC_KEY = getattr(settings, "PAYSTACK_PUBLIC_KEY", "")

paystack_gateway = paystack.PaystackGateway(secret_key=SECRET_KEY, public_key=PUBLIC_KEY)