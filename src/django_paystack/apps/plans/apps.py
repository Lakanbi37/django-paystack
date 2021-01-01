from django.utils.translation import gettext_lazy as _
from django.urls import path
from django_paystack.config import PaystackConfig
from django_paystack.core.loading import get_class


class PlansConfig(PaystackConfig):
    name = 'django_paystack.apps.plans'
    label = "plans"
    verbose_name = _('Plans')

    def ready(self):
        self.plan_create_api = get_class("plans.api.views", "PlanCreateAPIView")
        self.subscribe_api = get_class("plans.api.views", "SubscribeAPIView")
        self.enable_subcription_api = get_class("plans.api.views", "EnableSubscriptionAPIView")
        self.disable_subscription_api = get_class("plans.api.views", "DisableSubscriptionAPIView")

    def get_urls(self):
        urls = [
            path("create/", self.plan_create_api.as_view()),
            path("subscribe/", self.subscribe_api.as_view()),
            path("subcription/enable/", self.enable_subcription_api.as_view()),
            path("subscription/disable/", self.disable_subscription_api.as_view()),
        ]
        return self.post_process_urls(urls)
