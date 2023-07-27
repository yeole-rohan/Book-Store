from django.shortcuts import render, redirect
from .models import Order
import requests, base64
from django.http import JsonResponse
from Book.models import Book
from django.db.models import F
from Cart.models import Cart
from Wishlist.models import Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from famousbook.settings import EMAIL_HOST_USER as EMAIL_USER
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def orderDetailsFromUPI(request):
    print("order details view\n\n\n")
    if request.method == 'POST':
        # Handle the incoming S2S Callback here
        callback_data = request.POST
        print("initial", callback_data)
        callback_data = base64.b64decode(callback_data)
        print(callback_data, "callback data")
        return JsonResponse({'message': 'Callback received successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
@csrf_exempt
def successful(request):
    print("into successfull view\n\n\n", request.POST)
    if request.method == 'POST':
        status = request.POST.get("code")
        if status == 'PAYMENT_SUCCESS':
            # cart_items = Cart.objects.filter(user=request.user)
            # for cart in cart_items:
            #     if Book.objects.filter(id=cart.book.id, quantity__gte=cart.qty):
            #         Book.objects.select_for_update().filter(id=cart.book.id).update(quantity=F("quantity") - cart.qty)
            #         orderId = Order.objects.create(user=request.user, book=cart.book, qty=cart.qty,pickType=cart.pickType,deliveryAddress=cart.deliveryAddress,coupon_code=cart.coupon_code, charges=cart.charges, orderPlaced=True, shippingCharge=cart.shippingCharge,merchantTransactionId=request.POST['data']["merchantTransactionId"])
            messages.success(request, "Your Payment is successful.")
        elif status == 'PAYMENT_ERROR':
            messages.error(request, "Your Payment is successful.")
    return render(request, template_name="payment-successful.html", context={'message' : request.POST.get('message', '')})
    
    