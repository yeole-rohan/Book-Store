from django.db import models
from django.utils.translation import gettext_lazy as _
from Book.models import Book, CouponCode
from User.models import User, DeliveryAddress

class Cart(models.Model):
    PICKUPS = (
        ("self", "I will pick from store"),
        ("deliver", "Deliver to me")
    )
    PAYMENTTYPE = (
        ("cod", "Cash on Delivery"),
        ("online", "Online")
    )
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(_("Quantity"), default=1)
    pickType = models.CharField(_("Pick up type"),choices=PICKUPS, max_length=50, default="deliver")
    deliveryAddress = models.ForeignKey(DeliveryAddress, verbose_name=_("Delivery Address"), on_delete=models.CASCADE, blank=True, null=True)
    coupon_code = models.ForeignKey(CouponCode, verbose_name=_("Coupon Code"), on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(_("Cart created date"),auto_now_add=True)
    merchantTransactionId = models.TextField(_("Merchant Id"),default='', blank=True, null=True)
    last_updated = models.DateTimeField(_("Cart last updated"), auto_now=True)
    charges = models.PositiveBigIntegerField(_("Charges"), default=0)
    shippingCharge = models.PositiveIntegerField(_("Shipping Charge"), default=0)
    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return str(self.id)