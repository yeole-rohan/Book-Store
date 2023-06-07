from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetConfirmView, PasswordResetCompleteView
)
from . import views

urlpatterns = [
    path("info/", views.accountInfo, name="accountInfo"),
    path("login/", views.loginView, name="loginView"),
    path("signup/", views.signUp, name="signUp"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout')
]
