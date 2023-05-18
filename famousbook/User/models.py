from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    contactNumber = models.CharField(_("Contact Number"), max_length=12)
    created = models.DateTimeField(_("User created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("User last updated"), auto_now=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return str(self.id)

