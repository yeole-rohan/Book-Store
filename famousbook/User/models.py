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

class DeliveryAddress(models.Model):
    STATE = (
        ("AN", "Andaman and Nicobar Islands"),
        ("AP", "Andhra Pradesh"),
        ("AR", "Arunachal Pradesh"),
        ("AS", "Assam"),
        ("BR", "Bihar"),
        ("CH", "Chandigarh"),
        ("CG", "Chhattisgarh"),
        ("DN", "Dadra and Nagar Haveli"),
        ("DD", "Daman and Diu"),
        ("DL", "Delhi"),
        ("GA", "Goa"),
        ("GJ", "Gujarat"),
        ("HR", "Haryana"),
        ("HP", "Himachal Pradesh"),
        ("JK", "Jammu and Kashmir"),
        ("JH", "Jharkhand"),
        ("KA", "Karnataka"),
        ("KL", "Kerala"),
        ("LA", "Ladakh"),
        ("MP", "Madhya Pradesh"),
        ("MH", "Maharashtra"),
        ("MN", "Manipur"),
        ("ML", "Meghalaya"),
        ("MZ", "Mizoram"),
        ("NL", "Nagaland"),
        ("OR", "Odisha"),
        ("PY", "Puducherry"),
        ("PB", "Punjab"),
        ("RJ", "Rajasthan"),
        ("SK", "Sikkim"),
        ("TN", "Tamil Nadu"),
        ("TS", "Telangana"),
        ("TR", "Tripura"),
        ("UP", "Uttar Pradesh"),
        ("UK", "Uttarakhand"),
        ("WB", "West Bengal"),
    )
    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
    contactNumber = models.CharField(_("Contact Number"), max_length=12)
    name = models.CharField(_("Name"), max_length=50)
    address = models.CharField(_("Address"), max_length=300)
    city = models.CharField(_("City"), max_length=50)
    state = models.CharField(_("State"), choices=STATE, default="AN", max_length=100)
    pinCode = models.CharField(_("Pin Code"), max_length=10)
    landmark = models.CharField(_("Landmark"), max_length=50)
    class Meta:
        verbose_name = _("Delivery Address")
        verbose_name_plural = _("Delivery Address")

    def __str__(self):
        return self.address


class VerificationCode(models.Model):
    code = models.BigIntegerField(_("Code"))
    read = models.BooleanField(_("Read"))
    email = models.EmailField(_("Email"), max_length=254, blank=True, null=True)
    created = models.DateTimeField(_("Subscription created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Subscription last updated"), auto_now=True)

class Query(models.Model):
    PURPOSE = (
        ("delivery-charges", "Delivery charges"),
        ("delivery-time","Delivery time"),
        ("return-policy","Return policy")
    )
    purposeContact = models.CharField(_("Purpose of Contact"), choices=PURPOSE, max_length=50)
    message = models.TextField(_("Please State your massage here"))
    user = models.ForeignKey("User", verbose_name=_("User"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Query")
        verbose_name_plural = _("Query")

    def __str__(self):
        return self.purposeContact

