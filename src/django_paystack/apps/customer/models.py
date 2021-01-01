from django.conf import settings
from django.db import models
# Create your models here.


class CustomerManager(models.Manager):

    def add_customer(self, data):
        return self.create(**data)


class Customer(models.Model):
    customer_id = models.CharField(max_length=2000, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paystack_customer")
    customer_code = models.CharField(max_length=200)
    identified = models.BooleanField(default=False)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomerManager()

    class Meta:
        app_label = "customer"

    def __str__(self):
        return str(self.customer_code)