from django.contrib import admin

from .models import Category, ModeOfPayment, TransactionType, Transactions, Users

# Register your models here.
admin.site.register(Category)
admin.site.register(ModeOfPayment)
admin.site.register(TransactionType)
admin.site.register(Transactions)
admin.site.register(Users)
