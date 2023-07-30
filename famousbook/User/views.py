from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from random import random
from .models import User, VerificationCode, DeliveryAddress
from .forms import MyPasswordResetForm, UserForm, DeliveryAddressForm, QueryForm
from famousbook.settings import EMAIL_HOST_USER as EMAIL_USER
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
import requests
"""
This function handles the user account information page. It retrieves the user's information and displays it on the page. If the user submits a form with updated information, it updates the user's information and redirects them back to the account information page. If the form is not valid, it displays the errors on the page.
@param request - the HTTP request object
@return the rendered account-info.html template with the user's information and form.
"""
@login_required
def accountInfo(request):
    userForm =UserForm(instance=request.user)
    if request.method == "POST":
        userForm =UserForm(request.POST or None, instance=request.user)
        if userForm.is_valid():
            userForm.save()
            messages.success(request, "Profile Updated")
            return redirect("user:accountInfo")
        else:
            print(userForm.errors)
    return render(request, template_name="account-info.html", context={'form' : userForm})

"""
This function adds a delivery address to the user's account. It first initializes a `DeliveryAddressForm` with the user's full name and contact number. If the request method is POST, it checks if the form is valid. If it is, it saves the form with the user's information and redirects to the delivery address page. If the form is not valid, it prints the errors and returns the delivery address page with the form. 
@param request - the HTTP request
@return the delivery address page with the form
"""
@login_required
def deliveryAddressAdd(request):
    deliveryAddressForm =DeliveryAddressForm(initial={"name" : request.user.get_full_name, "contactNumber" : request.user.contactNumber})
    if request.method == "POST":
        deliveryAddressForm =DeliveryAddressForm(request.POST or None)
        if deliveryAddressForm.is_valid():
            deliveryAddressForm = deliveryAddressForm.save(commit=False)
            deliveryAddressForm.user = request.user
            pinCode = request.POST.get("pinCode")
            # Replace pin code with the desired pin code
            url = f'https://api.delhivery.com/c/api/pin-codes/json/?filter_codes={pinCode}'
            headers = {
                'Authorization': 'Token c724adf975113702c971cb923a7a0f4f85b36ecc'  # Replace YOUR_API_KEY_HERE with your actual API key
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if len(data['delivery_codes']) > 0:
                    deliveryAddressForm.save()
                    messages.success(request, "Address is serviable")
                    return redirect("user:deliveryAddress")
                else:
                    messages.error(request, "Address is not serviable, try diffrent")
                    return redirect("user:deliveryAddressAdd")
            else:
                messages.error(request, "Error while fetching pin code availability service")
            return redirect("user:deliveryAddress")
        else:
            print(deliveryAddressForm.errors)
    return render(request, template_name="delivery-address-add.html", context={'form' : deliveryAddressForm})

"""
This function allows a user to edit a delivery address. It takes in a request and an id of the address to be edited. It retrieves the address from the database using the id and creates a form with the retrieved address. If the request method is POST, it updates the form with the new data and saves it to the database. If the form is valid, it redirects the user to the delivery address page and displays a success message. If the form is not valid, it prints the errors and returns the same page with the form and errors displayed. 
@param request - the HTTP request object
@param id - the id of the delivery address to be edited
@return the rendered HTML template with the updated delivery address form.
"""
@login_required
def deliveryAddressEdit(request, id):
    editAddress = DeliveryAddress.objects.get(id=id)
    deliveryAddressForm =DeliveryAddressForm(instance=editAddress)
    if request.method == "POST":
        deliveryAddressForm =DeliveryAddressForm(request.POST or None, instance=editAddress)
        if deliveryAddressForm.is_valid():
            deliveryAddressForm = deliveryAddressForm.save(commit=False)
            pinCode = request.POST.get("pinCode")
            # Replace pin code with the desired pin code
            url = f'https://api.delhivery.com/c/api/pin-codes/json/?filter_codes={pinCode}'
            headers = {
                'Authorization': 'Token c724adf975113702c971cb923a7a0f4f85b36ecc'  # Replace YOUR_API_KEY_HERE with your actual API key
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if len(data['delivery_codes']) > 0:
                    deliveryAddressForm.save()
                    messages.success(request, "Address is serviable")
                    return redirect("user:deliveryAddress")
                else:
                    messages.error(request, "Address is not serviable, try diffrent")
                    return redirect("user:deliveryAddressEdit", id)
            else:
                messages.error(request, "Error while fetching pin code availability service")
            return redirect("user:deliveryAddressEdit", id)
        else:
            print(deliveryAddressForm.errors)
    return render(request, template_name="delivery-address-add.html", context={'form' : deliveryAddressForm})

"""
This function deletes a delivery address from the database and redirects the user to the delivery address page.
@param request - the HTTP request object
@param id - the id of the delivery address to be deleted
@returns a redirect to the delivery address page
"""
@login_required
def deliveryAddressDelete(request, id):
    try:
        editAddress = DeliveryAddress.objects.filter(id=id).delete()
        messages.success(request, "Address deleted.")
    except DeliveryAddress.DoesNotExist:
        messages.error(request, "Address not exist.")
    return redirect("user:deliveryAddress")

"""
Given a request, retrieve the delivery address for the user and render the delivery address page.
@param request - the request object
@return the delivery address page with the user's address information.
"""
@login_required
def deliveryAddress(request):
    getAddress = DeliveryAddress.objects.filter(user=request.user)
    return render(request, template_name="delivery-address.html", context={'getAddress' : getAddress})

"""
This function handles user contact requests. It renders a form for the user to fill out and submit. If the form is submitted, it validates the form data and saves it to the database. If the form is not valid, it prints the errors to the console. Finally, it renders the user-contact.html template with the form as context.
@param request - the HTTP request object
@return the rendered user-contact.html template with the form as context.
"""
@login_required
def userContact(request):
    queryForm =QueryForm()
    if request.method == "POST":
        queryForm =QueryForm(request.POST or None)
        if queryForm.is_valid():
            queryForm = queryForm.save(commit=False)
            queryForm.user = request.user
            purposeContact = request.POST.get("purposeContact")
            message = request.POST.get("message")
            queryForm.save()
            subject = "Contact Us Query"
            send_mail(subject, "{} is contacting for {} with {}".format(request.user.email,purposeContact.replace("-", " "), message ), EMAIL_USER, [EMAIL_USER],)
            messages.success(request, "Message Saved")
            return redirect("user:userContact")
        else:
            print(queryForm.errors)
    return render(request, template_name="user-contact.html", context={'form' : queryForm})

@login_required
def editPassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('user:editPassword')
        else:
            messages.error(request, 'Falied to update your password. Please check the errors.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, template_name="edit-password.html", context={'form' : form})


'''Returns new OTP'''
def getOTP():
    OTP = int(random() * 98765)
    if VerificationCode.objects.filter(code = OTP, read=True):
        getOTP()
    else:
        return OTP
    
'''Login view'''
def loginView(request):
    if request.user.is_authenticated:
        return redirect("book:home")
    email_or_mobile = ''
    isPassword, isMobile, hideNext = False, False, False
    if request.method == "POST":
        email_or_mobile = request.POST.get("email_or_mobile")
        password= request.POST.get("password")
        if email_or_mobile:
            if type(email_or_mobile) == str and "@" in email_or_mobile:
                try:
                    user = User.objects.get(email=email_or_mobile)
                    user = authenticate(request, username=user.username, password=password)
                    print("user", user)
                    if user is not None:
                        login(request, user)
                        return redirect("book:home")
                    else:
                        messages.error(request, "Entered wrong credentials.")
                except:
                    messages.error(request, "User not found.")
        else:
            messages.error(request, "Enter Email Id")
    return render(request, template_name="login.html", context={'email_or_mobile' : email_or_mobile, 'isMobile' : isMobile, 'isPassword' : isPassword, 'hideNext' : hideNext})


'''Sign Up View'''
def signUp(request):
    if request.user.is_authenticated:
        return redirect("book:home")
    email_or_mobile = ''
    isPassword, isMobile, hideNext = False, False, False
    if request.method == "POST" and "next-step" in request.POST:
        email_or_mobile = request.POST.get("email_or_mobile")
        if email_or_mobile:
            if type(email_or_mobile) == str and "@" in email_or_mobile:
                if User.objects.filter(email=email_or_mobile).exists():
                    messages.error(request, "Email Exists")
                    return redirect("user:signUp")
                else:
                    isPassword = True
                    hideNext = True
                    code = getOTP()
                    createCode = VerificationCode.objects.create(code=code, email=email_or_mobile, read=False)
                    messages.success(request, "OTP is sent on email")
                    if createCode:
                        subject = "Confirm your email address."
                        loginHTMLTemplate = render_to_string("email-template/email-verification-code.html", context={"OTP" : code }, )
                        body = strip_tags(loginHTMLTemplate)
                        send_mail(subject, body, EMAIL_USER, [email_or_mobile], html_message=loginHTMLTemplate)
            else:
                # TODO Create Signup with Mobile Number
                # isMobile =True
                # hideNext = True
                messages.error(request, "Enter valid email")
                return redirect("user:signUp")
        else:
            messages.error(request, "Enter Email Id")
            return redirect("user:signUp")

    if request.method == "POST" and "isPassword" in request.POST:
        email_or_mobile = request.POST.get("email_or_mobile")
        otp = request.POST.get("otp")
        password = request.POST.get("password")
        if otp:
            if VerificationCode.objects.filter(code=otp, email=email_or_mobile, read=False).exists():
                VerificationCode.objects.filter(code=otp, email=email_or_mobile, read=False).update(read=True)
                createuser = User.objects.create(email=email_or_mobile, username="user"+str(User.objects.last().id + 1 if User.objects.last() else 1))
                createuser.set_password(password)
                createuser.save()
                subject = "Welcome."
                body = "Hi {}, We welcome you to our platform, your username is {}. Happy Reading!".format(createuser.email, createuser.username)
                send_mail(subject, body, EMAIL_USER, [email_or_mobile], fail_silently=True)
                user = authenticate(request, username=createuser.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, 'Logged in')
                    return redirect("book:home")
            else:
                isPassword = True
                hideNext = True
                messages.error(request, "Verification code is invalid")
                # return redirect("user:signUp")
        else:
            isPassword = True
            hideNext = True
            messages.error(request, "Enter OTP")
            # return redirect("user:signUp")
        
    # TODO : Mobile User creation part pending
    if request.method == "POST" and "next-step" in request.POST and "isMobile" in request.POST:
        pass
    return render(request, template_name="signup.html", context={'email_or_mobile' : email_or_mobile, 'isMobile' : isMobile, 'isPassword' : isPassword, 'hideNext' : hideNext})

"""
This is a view for resetting a user's password. It inherits from Django's built-in `PasswordResetView` and adds some custom functionality.
"""
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    
    form_class = MyPasswordResetForm

    def form_valid(self, form):
        email_or_username = form.cleaned_data['email']
        if email_or_username:
            if "@" in email_or_username:
                self.success_message = "Email sent to {} double check if this is your email. you will receive email link to reset your login password.".format(email_or_username)
            else:
                self.success_message = "{} you will receive email link to reset your login password.".format(email_or_username)
        return super().form_valid(form)
    success_url = reverse_lazy('user:loginView')