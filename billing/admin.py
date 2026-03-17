from django.contrib import admin
from .models import Product,Purchase,PurchaseItem


admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)

# Register your models here.
