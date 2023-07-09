from django.shortcuts import render, redirect
from .models import Order
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
        featuredBooks = Book.objects.all()[:10]
    except:
        featuredBooks = Book.objects.all()
    wish_items = Wishlist.objects.filter(user=request.user)
    return render(request, template_name="my-orders.html", context={'myOrders' : myOrders, "featuredBooks" : featuredBooks, "wish_items" : wish_items})

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