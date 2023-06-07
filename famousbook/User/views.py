from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from random import random
from .models import User, VerificationCode
from famousbook.settings import EMAIL_HOST_USER as EMAIL_USER

'''User Account'''
def accountInfo(request):
    return render(request, template_name="account-info.html", context={})

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
                user = User.objects.get(email=email_or_mobile)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("book:home")
            # else:
            #     print("int")
            #     isMobile =True
            #     hideNext = True
        else:
            messages.error(request, "Enter Mobile or Email Id")
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
                    print(code)
                    VerificationCode.objects.create(code=code, email=email_or_mobile, read=False)
                    messages.success(request, "OTP is sent on email")
                    # if createCode:
                    #     subject = "Confirm your email address."
                    #     loginHTMLTemplate = render_to_string("email-template/email-verification-code.html", context={"OTP" : code }, )
                    #     body = strip_tags(loginHTMLTemplate)
                    #     send_mail(subject, body, EMAIL_USER, [email_or_mobile], html_message=loginHTMLTemplate)
            else:
                # TODO Create Signup with Mobile Number
                # isMobile =True
                # hideNext = True
                messages.error(request, "Enter valid email")
                return redirect("user:signUp")
        else:
            messages.error(request, "Enter Mobile or Email Id")
            return redirect("user:signUp")

    if request.method == "POST" and "isPassword" in request.POST:
        email_or_mobile = request.POST.get("email_or_mobile")
        otp = request.POST.get("otp")
        password = request.POST.get("password")
        print(otp, password)
        if otp:
            print(VerificationCode.objects.filter(code=otp, email=email_or_mobile, read=False).exists())
            if VerificationCode.objects.filter(code=otp, email=email_or_mobile, read=False).exists():
                VerificationCode.objects.filter(code=otp, email=email_or_mobile, read=False).update(read=True)
                createuser = User.objects.create(email=email_or_mobile, username="user"+str(User.objects.last().id + 1 if User.objects.last() else 1))
                createuser.set_password(password)
                createuser.save()
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