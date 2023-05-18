from django.db import models
from django.utils.translation import gettext_lazy as _
from Book.models import Book
from User.models import User

class Wishlist(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, default="")
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    created = models.DateTimeField(_("Wishlist created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Wishlist last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")

    def __str__(self):
        return str(self.id)
