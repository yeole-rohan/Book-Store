from django.urls import path
from . import views

urlpatterns = [
    path("contact/", views.contactUs, name="contactUs"),
    path("about/", views.aboutUs, name="aboutUs")
]
