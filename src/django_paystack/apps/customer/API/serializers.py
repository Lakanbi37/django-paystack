from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from rest_framework import serializers
from ..models import Customer

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]


_UserSerializer = getattr(settings, "DJANGO_PAYSTACK_USER_SERIALIZER", "")
if _UserSerializer != "":
    UserSerializer = import_string(_UserSerializer)
else:
    UserSerializer = UserModelSerializer


class CustomerModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"
