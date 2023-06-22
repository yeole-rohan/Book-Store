from django import forms
from .models import User, DeliveryAddress, Query
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
