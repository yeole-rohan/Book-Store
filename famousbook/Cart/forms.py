from django import forms

class PromoCodeForm(forms.Form):
    promoCode = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={"placeholder" : "Enter Promo code"}))

class DeliveryAddressForm(forms.Form):
    PICKUPS = (
        ("self", "I will pick from store"),
        ("deliver", "Deliver to me")
    )
    pickup = forms.ChoiceField(label="Select pick up type", initial="deliver", choices=PICKUPS, required=True)
