from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import User, DeliveryAddress, Query
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class SignInForm(forms.Form):
    email_or_mobile = forms.CharField( max_length=50, required=True)

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "contactNumber")

class DeliveryAddressForm(forms.ModelForm):
    
    class Meta:
        model = DeliveryAddress
        fields = ("name", "contactNumber", "address", "city", "state", "landmark", "pinCode")
class QueryForm(forms.ModelForm):
    
    class Meta:
        model = Query
        fields = ("purposeContact","message")

class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label="Email or Username", max_length=256, required=False, help_text="You can enter username or email id of your account. make sure its correct otherwise, you may not receive an reset email.")

    def get_username_or_email_users(self, username_or_email):
        return list(User.objects.filter(Q(contactNumber__iexact=username_or_email) | Q( email__iexact=username_or_email)))

    def save(self, *args, **kwargs):
        username_or_email = self.cleaned_data.get("email")

        users_emails = self.get_username_or_email_users(username_or_email)
        current_site = get_current_site(kwargs.get("request"))
        token_generator = kwargs.get("token_generator")
        extra_email_context = kwargs.get("extra_email_context")
        use_https = kwargs.get("use_https")
        site_name = current_site.name
        domain = current_site.domain
        print(domain, site_name, use_https)
        if users_emails:
            for user in users_emails:

                context = { 'email': user.email, 'domain': domain, 'site_name': site_name, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'user': user, 'token': token_generator.make_token(user), 'protocol': 'https' if use_https else 'http', **(extra_email_context or {}), }

                self.send_mail( kwargs.get('subject_template_name'), kwargs.get('email_template_name'), context, "admin@famousbookshop.in", user.email, html_email_template_name=kwargs.get('html_email_template_name'), )
