from django.urls import path
from . import views

"""
This code defines a URL pattern for a Wishlist application.
"""
urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.addToWishList, name="addToWishList"),
    path("delete/<int:id>/", views.deleteWishListBook, name="deleteWishListBook"),
    path("to-cart/<int:itemId>/", views.toCart, name="toCart"),
]
