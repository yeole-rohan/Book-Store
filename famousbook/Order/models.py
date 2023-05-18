from django.db import models
from django.utils.translation import gettext_lazy as _
from Book.models import Book

class Order(models.Model):
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    created = models.DateTimeField(_("Order created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Order last updated"), auto_now=True)
    

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.id)

