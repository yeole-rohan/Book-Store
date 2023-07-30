from django.shortcuts import render, redirect
from .models import Order
import requests, base64, json, hashlib
from django.http import JsonResponse
from Book.models import Book, PinCodeStateCharges
from django.db.models import F
from User.models import DeliveryAddress
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
    print("order details view\n\n\n", request)
    if request.method == 'POST':
        
        # Handle the incoming S2S Callback here
        jsonData = json.loads(str(request.body).replace("b'{", "{").replace("}'", "}")).get("response")
        print("initial", jsonData)

        try:
            # Decode the base64 callback data using 'latin-1'
            decoded_data = base64.b64decode(jsonData).decode('utf-8')
            print(decoded_data, "decoded_data")
            decoded_data = json.loads(decoded_data)
            print("json decoded_data", decoded_data)
            if decoded_data.get('code') == "PAYMENT_SUCCESS":
                idList = []
                failedCheckout = []
                cart_items = Cart.objects.filter(merchantTransactionId=decoded_data['data']['merchantTransactionId'])
                email = cart_items.first().user.email
                deliveryAddress=DeliveryAddress.objects.get(id=list(cart_items.values_list("deliveryAddress", flat=True))[0])
                print("deliveryAddress",deliveryAddress)
                pinCode = PinCodeStateCharges.objects.get(state__iexact=deliveryAddress.state)
                for cart in cart_items:
                    if Book.objects.filter(id=cart.book.id, quantity__gte=cart.qty).count():
                        Book.objects.select_for_update().filter(id=cart.book.id).update(quantity=F("quantity") - cart.qty)
                        orderId = Order.objects.create(user=cart.user, book=cart.book, qty=cart.qty,pickType=cart.pickType,deliveryAddress=cart.deliveryAddress,coupon_code=cart.coupon_code, charges=cart.charges, orderPlaced=True, shippingCharge=cart.shippingCharge,merchantTransactionId=decoded_data['data']["merchantTransactionId"], transactionId=decoded_data['data']['transactionId'], totalAmount=float(decoded_data['data']['amount']/100), state=decoded_data['data']['state'], paymentType="online",deliveryTime =pinCode.deliveryEstimate, dispatchTime=pinCode.dispatchTime)
                        idList.append(orderId.id)
                    else:
                        orderId = Order.objects.create(user=cart.user, book=cart.book, qty=cart.qty,pickType=cart.pickType,deliveryAddress=cart.deliveryAddress,coupon_code=cart.coupon_code, charges=cart.charges, shippingCharge=cart.shippingCharge, payType="COD", paymentType="online",orderPlaced=False, deliveryTime =pinCode.deliveryEstimate, dispatchTime=pinCode.dispatchTime)
                        failedCheckout.append(orderId.id)

                if failedCheckout:
                    subject = "Failed Orders for {}".format(email)
                    loginHTMLTemplate = render_to_string("email-template/order.html", context={"orderList" : Order.objects.filter(id__in=failedCheckout).order_by("-created"), "isFailed":True })
                    body = strip_tags(loginHTMLTemplate)
                    send_mail(subject, body, EMAIL_USER, [email], html_message=loginHTMLTemplate)
                    send_mail(subject, body, EMAIL_USER, [EMAIL_USER], html_message=loginHTMLTemplate)
                subject = "Order Confirmation for {}".format(email)
                loginHTMLTemplate = render_to_string("email-template/order.html", context={"orderList" : Order.objects.filter(id__in=idList).order_by("-created"), "isFailed":False }, )
                body = strip_tags(loginHTMLTemplate)
                send_mail(subject, body, EMAIL_USER, [email], html_message=loginHTMLTemplate)
                send_mail(subject, body, EMAIL_USER, [EMAIL_USER], html_message=loginHTMLTemplate)
                cart_items.delete()
            elif decoded_data.get('code') == "PAYMENT_ERROR":
                print("users payment failled")
        except UnicodeDecodeError:
            return JsonResponse({"error": "Error decoding callback data."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

@csrf_exempt
def successful(request):
    print("into successfull view\n\n\n", request.POST)
    if request.method == 'POST':
        flag = request.POST.get("code")
        if flag == 'PAYMENT_SUCCESS':
            messages.success(request, "Your Payment is successful. Check your mail for details")
        elif flag == 'PAYMENT_ERROR':
            messages.error(request, "Your Payment is failed.")
        return redirect("order:successful")
    return render(request, template_name="payment-successful.html", context={})
    
    