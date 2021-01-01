from django.contrib import admin
from .models import Transfer, Recipient, AccountDetails
# Register your models here.

admin.site.register(Transfer)
admin.site.register(Recipient)
admin.site.register(AccountDetails)
