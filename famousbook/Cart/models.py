from django.db import models
from django.utils.translation import gettext_lazy as _
from Book.models import Book
from User.models import User
from User.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(_("Quantity"), default=1)
    created = models.DateTimeField(_("Cart created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Cart last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return str(self.id)