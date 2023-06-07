from django import forms

class SignInForm(forms.Form):
    email_or_mobile = forms.CharField( max_length=50, required=True)
