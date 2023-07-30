from django.contrib import admin
from .models import ContactUs

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("id","fullName", "mobileNumer","emailId", "address", "user","purposeOfContact", "description", "created", "last_updated")
    list_display_links = ("fullName", )

