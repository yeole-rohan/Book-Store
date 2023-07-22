from django.urls import path
from . import views

"""
This code defines a URL pattern for a Cart application.
"""
urlpatterns = [
    path("", views.myOrders, name="myOrders"),
    path("cancel-order/<int:id>/", views.cancelOrder, name="cancelOrder"),
    path("track-order/<int:tId>/", views.trackOrder, name="trackOrder"),
]
