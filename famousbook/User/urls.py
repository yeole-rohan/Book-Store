from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetConfirmView, PasswordResetCompleteView
)
from . import views

urlpatterns = [
    path('forget-password/', views.ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="password_reset_change.html"), name="password_reset_confirm"),
    path("info/", views.accountInfo, name="accountInfo"),
    path("login/", views.loginView, name="loginView"),
    path("signup/", views.signUp, name="signUp"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path("delivery-address/", views.deliveryAddress, name="deliveryAddress"),
    path("delivery-address/create/", views.deliveryAddressAdd, name="deliveryAddressAdd"),
    path("delivery-address/edit/<int:id>/", views.deliveryAddressEdit, name="deliveryAddressEdit"),
    path("delivery-address/delete/<int:id>/", views.deliveryAddressDelete, name="deliveryAddressDelete"),
    path("user/contact/", views.userContact, name="userContact"),
    path('change-password/', views.editPassword, name='editPassword'),
]
