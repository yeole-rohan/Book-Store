from django.shortcuts import render, redirect
from .models import Order
import requests
from Book.models import Book
from Wishlist.models import Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from famousbook.settings import EMAIL_HOST_USER as EMAIL_USER

@login_required
def myOrders(request):
    myOrders = Order.objects.filter(user=request.user).order_by("-created")
    try:
        featuredBooks = Book.objects.filter(isPublished=True, quantity__gt=0)[:10]
    except:
        featuredBooks = Book.objects.filter(isPublished=True, quantity__gt=0)
    try:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True, quantity__gt=0)[:10]
    except:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True, quantity__gt=0)
    wish_items = Wishlist.objects.filter(user=request.user)
    return render(request, template_name="my-orders.html", context={'bestSeller':bestSeller,'myOrders' : myOrders, "featuredBooks" : featuredBooks, "wish_items" : wish_items})

@login_required
def trackOrder(request, tId):
    url = f'https://track.delhivery.com/api/v1/packages/json/?waybill={tId}'
    headers = {
        'Authorization': 'Token c724adf975113702c971cb923a7a0f4f85b36ecc'  # Replace YOUR_API_KEY_HERE with your actual API key
    }

    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        orderStatus = res.json()
    else:
        orderStatus = {} 
    return render(request, template_name="track-order.html", context={'orderStatus':orderStatus, 'tId' :tId})

@login_required
def cancelOrder(request, id):
    Order.objects.filter(id=id).update(orderStatus="cancel")
    subject = "Order Cancellation"
    loginHTMLTemplate = render_to_string("email-template/order-cancellation.html", context={"order" : Order.objects.get(id=id, orderStatus="cancel") }, )
    body = strip_tags(loginHTMLTemplate)
    send_mail(subject, body, EMAIL_USER, [request.user.email], html_message=loginHTMLTemplate)
    send_mail(subject, body, EMAIL_USER, [EMAIL_USER], html_message=loginHTMLTemplate)
    messages.success(request, "Order has been cancelled")
    return redirect("order:myOrders")