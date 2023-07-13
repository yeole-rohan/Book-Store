from django.shortcuts import render, redirect
from django.core.mail import send_mail
from famousbook.settings import EMAIL_HOST_USER as EMAIL_USER
from .forms import ContactUsForm
from django.contrib import messages

def contactUs(request):
    contactUsForm = ContactUsForm()
    if request.method == "POST":
        contactUsForm = ContactUsForm(request.POST or None)
        if contactUsForm.is_valid():
            contactUsForm = contactUsForm.save(commit=False)
            if request.user.is_authenticated:
                contactUsForm.user = request.user
            fullName = request.POST.get("fullName")
            mobileNumer = request.POST.get("mobileNumer")
            emailId = request.POST.get("emailId")
            address =  request.POST.get("address")
            description = request.POST.get("description")
            purposeOfContact = request.POST.get("purposeOfContact")
            contactUsForm.save()
            subject = "Contact Us"
            send_mail(subject, "{} is contacting with {}, {}, {} for {} with {}".format(fullName,mobileNumer,emailId,address,description, purposeOfContact.replace("-", " ")), EMAIL_USER, [EMAIL_USER],)
            messages.success(request, "Thanks for contacting.")
            return redirect("staticPages:contactUs")
        else:
            print(contactUsForm.errors)
    return render(request, template_name="contact-us.html", context={'contactUsForm' : contactUsForm})

def aboutUs(request):
    return render(request, template_name="about-us.html", context={})
