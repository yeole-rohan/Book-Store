from django.contrib import admin
from .models import User, DeliveryAddress, VerificationCode, Query
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name","last_name", "contactNumber", "created", "last_updated")
    list_display_links = ("email","username" )

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "contactNumber", "name","address", "city", "state", "pinCode", "landmark")
    list_display_links = ("name", )

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("id","code", "read","email", "created", "last_updated")
    list_display_links = ("code", )

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("id","purposeContact", "message","user")
    list_display_links = ("purposeContact", )
