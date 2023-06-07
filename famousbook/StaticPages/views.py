from django.shortcuts import render
from .forms import ContactUsForm
def contactUs(request):
    contactUsForm = ContactUsForm()
    return render(request, template_name="contact-us.html", context={'contactUsForm' : contactUsForm})

def aboutUs(request):
    return render(request, template_name="about-us.html", context={})
