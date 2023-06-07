from django import forms
from .models import ContactUs


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ("fullName", "mobileNumer", "emailId", "address", "purposeOfContact", "description",)
        widgets = {
            "fullName" : forms.TextInput(attrs={"placeholder" : "Enter your Name here"}),
            "mobileNumer" : forms.NumberInput(attrs={"placeholder" : "+91 8659743822"}),
            "emailId" : forms.EmailInput(attrs={"placeholder" : "yourmailid@gamil.ccom"}),
            "address" : forms.Textarea(attrs={"placeholder" : "Add Address here"}),
            "description" : forms.Textarea(attrs={"placeholder" : "Max 500 Characters"})
        }
        labels = {
            "fullName" : "Full Name",
            "mobileNumer" : "Mobile No.",
            "emailId" : "E-Mail Id",
            "address" : "Address",
            "purposeOfContact" : "Purpose of Contact*",
            "description" : "Purpose of Contact*"
        }