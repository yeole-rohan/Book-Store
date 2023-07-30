from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'qty', 'pickType', 'deliveryAddress', 'coupon_code','merchantTransactionId', 'shippingCharge', 'charges', 'created', 'last_updated')
    list_display_links = ("book",)
    list_filter = ('created', 'last_updated')
    search_fields = ('user__username', 'book__title')
    readonly_fields = ('created', 'last_updated')
