from django.contrib import admin
from .models import Source, SubAccount, TransactionSplit, SplitSubAccount
# Register your models here.


class SubAccountInline(admin.TabularInline):
    model = SplitSubAccount


class TransactionSplitAdmin(admin.ModelAdmin):
    inlines = [SubAccountInline]

    class Meta:
        model = TransactionSplit


admin.site.register(Source)
admin.site.register(SubAccount)
admin.site.register(TransactionSplit, TransactionSplitAdmin)
admin.site.register(SplitSubAccount)
