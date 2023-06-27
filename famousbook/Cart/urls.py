from django.urls import path
from . import views

"""
This code defines a URL pattern for a Cart application.
"""
urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:cartId>/", views.remove_cart_item, name="remove_cart_item"),
    path("update/quantity/", views.update_quantity, name="update_quantity"),
    path("to-wishlist/<int:itemId>/", views.toWishList, name="toWishList"),
    path("select-address/", views.selectAddress, name="selectAddress"),
    path("overview/", views.overview, name="overview",),
    path("update/ship-charge/", views.update_charge, name="update_charge")
]
