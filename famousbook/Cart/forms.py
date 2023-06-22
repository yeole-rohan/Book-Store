from django import forms

class PromoCodeForm(forms.Form):
    promoCode = forms.CharField(label="", max_length=50, required=False)
