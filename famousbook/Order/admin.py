
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'qty', 'orderStatus', 'pickType','merchantTransactionId', 'transactionId', 'payType', 'totalAmount', 'state', 'shippingCharge', 'deliveryAddress', 'coupon_code', 'paymentType','trackingNumber', 'orderPlaced','dispatchTime', 'deliveryTime', 'orderStatus', 'charges', 'created', 'last_updated')
    list_display_links = ("book",)
    list_filter = ('created', 'last_updated')
    search_fields = ('user__username', 'book__title')
    readonly_fields = ('created', 'last_updated')
