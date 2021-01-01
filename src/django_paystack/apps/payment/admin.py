from django.contrib import admin
from .models import Source, SubAccount, TransactionSplit
# Register your models here.


class TransactionSplitAdmin(admin.ModelAdmin):

    class Meta:
        model = TransactionSplit


admin.site.register(Source)
admin.site.register(SubAccount)
admin.site.register(TransactionSplit, TransactionSplitAdmin)
