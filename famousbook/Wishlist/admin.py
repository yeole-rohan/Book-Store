from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id","user", "book", "created", "last_updated")
    list_display_links = ("user", )

