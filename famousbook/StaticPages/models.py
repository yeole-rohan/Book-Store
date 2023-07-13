from django.db import models
from django.utils.translation import gettext_lazy as _
from User.models import User
'''Update for logged in user'''
class ContactUs(models.Model):
    PURPOSE = (
        ("", "Select the reason"),
        ("payment-related", "Payment Related"),
        ("order-related", "Order Related"),
        ("courier-related", "Courier Related"),
        ("affiliate-related", "Affiliate Related"),
        ("authors-publishers-related", "Authors/Publishers Related"),
        ("corporate-order-bulk-sales", "Corporate Order/Bulk Sales"),
        ("business-related", "Business Related"),
        ("features-suggestions-feedback", "Features,suggestions & Feedback"),
        ("any-other", "Any Other"),
    )
    fullName = models.CharField(_("Full Name"), max_length=250)
    mobileNumer = models.CharField(_("Mobile Number"), max_length=13)
    emailId = models.EmailField(_("E-Mail Id"), max_length=254)
    address = models.TextField(_("Address"))
    user = models.ForeignKey(User, verbose_name=_("Contact Person"), on_delete=models.CASCADE, blank=True, null=True)
    purposeOfContact = models.CharField(_("Purpose of Contact"), choices=PURPOSE, max_length=250)
    description =models.CharField(_("Please State your massage here"), max_length=500)
    created = models.DateTimeField(_("created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("last updated"), auto_now=True)
    class Meta:
        verbose_name = _("ContactUs")
        verbose_name_plural = _("ContactUs")

    def __str__(self):
        return self.fullName