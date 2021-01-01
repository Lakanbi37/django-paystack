from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_paystack.core.loading import get_model
from django_paystack.utils.gateway import paystack_gateway

Customer = get_model("customer", "Customer")

User = get_user_model()


def create_paystack_customer(instance):
    user_data = dict(
        email=instance.email,
        first_name=instance.first_name,
        last_name=instance.last_name
    )
    response = paystack_gateway.Customer.create(user_data)
    customer = Customer.objects.create(
        user=instance,
        customer_id=response["data"]["id"],
        customer_code=response["data"]["customer_code"],
        identified=response["data"]["identified"],
    )
    return customer


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, *args, **kwargs):
    if created:
        create_paystack_customer(instance)
    customer_exists = Customer.objects.get(user=instance).exists()
    if not created and not customer_exists:
        create_paystack_customer(instance)
