from django.contrib import admin
from .models import Transaction, History, Log
# Register your models here.

admin.site.register(Transaction)
admin.site.register(History)
admin.site.register(Log)
