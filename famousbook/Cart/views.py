from django.http import JsonResponse
from django.contrib import messages
from Book.models import Book
import json, datetime, requests, base64, hashlib, uuid
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, CouponCode
from Order.models import Order
from Wishlist.models import Wishlist
from Book.models import PinCodeStateCharges
from User.models import DeliveryAddress
from .forms import PromoCodeForm, DeliveryAddressForm, ShippingChargesForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from famousbook.settings import EMAIL_HOST_USER as EMAIL_USER, PHONEPAY_URL, PHONEPAY_MERCHANT_ID, PHONEPAY_SALT_KEY

"""
This function adds a book to the user's cart. If the user is authenticated, the book is added to their cart in the database. If the user is not authenticated, the book is added to their cart in the session. If the book is already in the cart, the function returns a message indicating that the book is already in the cart.
@param request - the HTTP request object
@param book_id - the ID of the book to add to the cart
@return a JSON response indicating whether the book was successfully added to the cart and any relevant messages
"""
def add_to_cart(request):
    if request.method=="POST":
        book_id = request.POST.get("book_id")
        try:
            book = Book.objects.get(id=int(book_id))
        except Book.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Book does not exist.'})

        if request.user.is_authenticated:
            cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
            if not created:
                return JsonResponse({'success': False, 'message': 'Book is already in your cart.'})
            
            return JsonResponse({'success': True, 'message': 'Book added to cart.', "cartCount" : Cart.objects.filter(user=request.user).exclude(book__quantity__lte=0).count()})
        else:
            cart_items = []
            cart_cookie = request.COOKIES.get('cart')

            if cart_cookie:
                cart_items = json.loads(cart_cookie)
            if not int(book_id) in cart_items:
                cart_items.append(book.id)
            else:
                return JsonResponse({'success': False, 'message': 'Book is already in your cart.'})
        
            response = JsonResponse({'success': True, 'message': 'Book added to cart.', "cartCount" : len(cart_items)})
            response.set_cookie('cart', json.dumps(cart_items))
            return response
    return JsonResponse({'success': False, 'message': 'Failed to add in your cart.'})


"""
This function is used to display the contents of the cart. It first checks if the user is authenticated. If the user is authenticated, it retrieves the cart items from the database. If the user is not authenticated, it checks if there is a cart cookie in the request. If there is a cart cookie, it retrieves the cart items from the cookie. Finally, it renders the cart.html template with the cart items as context.
@param request - the HTTP request object
@return the rendered cart.html template with the cart items as context.
"""

def view_cart(request):
    cart_items = []
    amountPayable = {}
    wish_items = ''
    promoCodeForm = PromoCodeForm()
    try:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True, quantity__gt=0)[:10]
    except:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True, quantity__gt=0)
    try:
        featuredBooks = Book.objects.filter(isPublished=True, quantity__gt=0)[:10]
    except:
        featuredBooks = Book.objects.filter(isPublished=True, quantity__gt=0)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_items.filter(product__quantity__lte=0).delete()
        wish_items = Wishlist.objects.filter(user=request.user)
        amountPayable = paymentCost(cart_items, None)
        if request.method == "POST" and "coupon" in request.POST:
            promoCodeForm = PromoCodeForm(request.POST or None)
            if promoCodeForm.is_valid():
                code = request.POST.get('promoCode')
                # private Coupon Code
                if CouponCode.objects.filter(user=request.user, coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now()).exists():
                    coupon = CouponCode.objects.get(user=request.user, coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now())
                    Cart.objects.filter(user=request.user).update(coupon_code=coupon)
                    amountPayable = paymentCost(cart_items, None)
                elif CouponCode.objects.filter(coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now()).exists():
                    coupon = CouponCode.objects.get(coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now())
                    Cart.objects.filter(user=request.user).update(coupon_code=coupon)
                    amountPayable = paymentCost(cart_items, None)
                else:
                    messages.error(request, "Promocode is expired.")
    elif 'cart' in request.COOKIES:
        cart_cookie = request.COOKIES.get('cart')
        print(cart_cookie)
        if cart_cookie:
            cart_ids = json.loads(cart_cookie)
            print("cart_ids", cart_ids)
            cart_items = Book.objects.filter(isPublished=True, id__in=cart_ids,quantity__gt=0)
            print(cart_items)
    return render(request, 'cart.html', context={'bestSeller':bestSeller, 'featuredBooks':featuredBooks,'cart_items': cart_items, 'wish_items' : wish_items, "amountPayable" : amountPayable, 'promoCodeForm' : promoCodeForm})

def paymentCost(cart_items, pinCode):
    print(pinCode, "pinCode")
    amountPayable = {}
    discount_percentage = list(cart_items.values_list("coupon_code__discount_percentage", flat=True))
    mrpTotal, discount, totalPayable, withOutDiscount, couponDiscount, mumbaiCharge, india, east, shippingAmount = 0, 0, 0, 0, 0, 0, 0, 0, 0
    isFree = False
    totalCartItems = cart_items.aggregate(totalQuantity = Sum("qty"))
    firstCart = cart_items.first()
    
    for item in cart_items:
        print(item.book.price, "item.book.price \n\n\n")
        mrpTotal += int(item.book.price * item.qty)
        if item.book.discountPrice:
            discount += round(float(item.book.price - item.book.discountPrice), 2)
        else:
            withOutDiscount += float(item.book.price)
    print()
    totalPayable = mrpTotal - discount

    print(totalCartItems, "totalCartItems", mrpTotal, totalPayable, discount, withOutDiscount )
    if pinCode:
        print(pinCode.freeShippingOn)
        if pinCode.freeShippingOn:
            print("inside",totalCartItems['totalQuantity'] <= 3 and mrpTotal <= pinCode.freeShippingOn)
            if totalCartItems['totalQuantity'] <= 3 and mrpTotal <= pinCode.freeShippingOn:
                shippingAmount = int(pinCode.initialCharge)
                print("shippingAmount calculated inside", shippingAmount)
            elif totalCartItems['totalQuantity'] > 3 and totalCartItems['totalQuantity'] <= 6 and mrpTotal <= pinCode.freeShippingOn:
                shippingAmount = int(pinCode.initialCharge + pinCode.threeBookCharge)
            elif totalCartItems['totalQuantity'] > 6 and mrpTotal <= pinCode.freeShippingOn:
                maxCharge = int(int(totalCartItems['totalQuantity'] - 6) / 3) * pinCode.sixBookCharge
                if maxCharge:
                    shippingAmount = int(pinCode.initialCharge + pinCode.threeBookCharge + maxCharge)
                else:
                    shippingAmount = int(pinCode.initialCharge + pinCode.threeBookCharge + pinCode.sixBookCharge)
            else:
                shippingAmount = 0
                isFree = True
            print("shippingAmount calculated", shippingAmount)
        else:
            if totalCartItems['totalQuantity'] <= 3:
                shippingAmount = int(pinCode.initialCharge)
            elif totalCartItems['totalQuantity'] > 3 and totalCartItems['totalQuantity'] <= 6:
                shippingAmount =int(pinCode.initialCharge + pinCode.threeBookCharge)
            elif totalCartItems['totalQuantity'] > 6:
                maxCharge = int(int(totalCartItems['totalQuantity'] - 6) / 3) * pinCode.sixBookCharge
                if maxCharge:
                    shippingAmount = int(pinCode.initialCharge + pinCode.threeBookCharge + maxCharge)
                else:
                    shippingAmount = int(pinCode.initialCharge + pinCode.threeBookCharge + pinCode.sixBookCharge)


    if discount_percentage and not discount_percentage[0] == None:
        print(totalPayable * float(discount_percentage[0]/100), "how much")
        couponDiscount = totalPayable * float(discount_percentage[0]/100)
        totalPayable -= couponDiscount
        print("minus coupon", totalPayable)
    
    cart_items.update(shippingCharge = int(shippingAmount))
    amountPayable['mrpTotal'] = mrpTotal
    amountPayable['totalDiscount'] = round(discount,2)
    amountPayable['totalSaving'] = round(float(discount + couponDiscount), 2)
    amountPayable["couponDiscount"] = round(couponDiscount, 2)
    print(round(float(totalPayable + shippingAmount), 2), "round")
    amountPayable['totalPayable'] = round(float(totalPayable + shippingAmount), 2)
    amountPayable["shippingAmount"] = shippingAmount
    amountPayable["isFree"] = isFree
    return amountPayable

@login_required
def selectAddress(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items.filter(product__quantity__lte=0).delete()
    amountPayable = paymentCost(cart_items, None)
    addressList = DeliveryAddress.objects.filter(user=request.user)
    deliveryAddressForm = DeliveryAddressForm()
    if request.method=="POST":
        deliveryAddressForm = DeliveryAddressForm(request.POST or None)
        if deliveryAddressForm.is_valid():
            deliveryType= request.POST.get("pickup")
            if deliveryType == "self":
                Cart.objects.filter(user=request.user).update(
                    pickType=deliveryType)
            else:
                deliveryAddress=DeliveryAddress.objects.get(id=request.POST.get("address"))
                pinCharge = PinCodeStateCharges.objects.get(state=deliveryAddress.state)
                Cart.objects.filter(user=request.user).update(
                    deliveryAddress=deliveryAddress, shippingCharge=pinCharge.initialCharge)
            return redirect("cart:overview")
    return render(request, 'selectAddress.html', context={"amountPayable" : amountPayable, 'addressList' : addressList, 'deliveryAddressForm' :deliveryAddressForm})

@login_required
def overview(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items.filter(product__quantity__lte=0).delete()
    merchantId = PHONEPAY_MERCHANT_ID
    deliveryAddress=DeliveryAddress.objects.get(id=list(cart_items.values_list("deliveryAddress", flat=True))[0])
    print("deliveryAddress",deliveryAddress)
    pinCode = PinCodeStateCharges.objects.get(state__iexact=deliveryAddress.state)
    amountPayable = paymentCost(cart_items, pinCode)
    failedCheckout = []
    pickUp = cart_items.first().pickType
    # charge = cart_items.first().charges
    # if charge:
    #     shippingChargesForm = ShippingChargesForm(initial={"charges" : "".join(charge)})
    # else:
    #     shippingChargesForm = ShippingChargesForm()
    if request.method=="POST" and "COD" in request.POST:
        idList = []
        merchantTransactionId = generate_merchant_transaction_id(merchantId)
        for cart in cart_items:
            if Book.objects.filter(id=cart.book.id, quantity__gte=cart.qty).count():
                Book.objects.select_for_update().filter(id=cart.book.id).update(quantity=F("quantity") - cart.qty)
                orderId = Order.objects.create(user=request.user, book=cart.book, qty=cart.qty,pickType=cart.pickType,deliveryAddress=cart.deliveryAddress,coupon_code=cart.coupon_code, charges=cart.charges, orderPlaced=True, shippingCharge=cart.shippingCharge, payType="COD", merchantTransactionId=merchantTransactionId,deliveryTime =pinCode.deliveryEstimate, dispatchTime=pinCode.dispatchTime)
                idList.append(orderId.id)
            else:
                orderId = Order.objects.create(user=request.user, book=cart.book, qty=cart.qty,pickType=cart.pickType,deliveryAddress=cart.deliveryAddress,coupon_code=cart.coupon_code, charges=cart.charges, orderPlaced=False, shippingCharge=cart.shippingCharge, payType="COD", merchantTransactionId=merchantTransactionId, deliveryTime =pinCode.deliveryEstimate, dispatchTime=pinCode.dispatchTime)
                failedCheckout.append(orderId.id)
        if failedCheckout:
            subject = "Failed Orders for {}".format(request.user.email)
            loginHTMLTemplate = render_to_string("email-template/order.html", context={"orderList" : Order.objects.filter(id__in=failedCheckout).order_by("-created"), "isFailed":True })
            body = strip_tags(loginHTMLTemplate)
            send_mail(subject, body, EMAIL_USER, [request.user.email], html_message=loginHTMLTemplate)
            send_mail(subject, body, EMAIL_USER, [EMAIL_USER], html_message=loginHTMLTemplate)
            messages.warning(request, "Some order failed to place due order quantity. We have sent you seperate mail")
        else:
            messages.success(request, "Your order has been placed. Please check your mail.")
        subject = "Order Confirmation for {}".format(request.user.email)
        loginHTMLTemplate = render_to_string("email-template/order.html", context={"orderList" : Order.objects.filter(id__in=idList).order_by("-created"), "isFailed":False }, )
        body = strip_tags(loginHTMLTemplate)
        send_mail(subject, body, EMAIL_USER, [request.user.email], html_message=loginHTMLTemplate)
        send_mail(subject, body, EMAIL_USER, [EMAIL_USER], html_message=loginHTMLTemplate)
        cart_items.delete()
        return redirect("order:myOrders")
        
    if request.method=="POST" and "UPI" in request.POST:
        response = isPaymentRequest(merchantId, amountPayable['totalPayable'])
        print(response, "response, hit upi")
        res = response.json()
        print(res, "res")
        if response.status_code == 200:
            print("Payment request successful.")
            res = response.json()
            print(res, "res")
            if res['success']:
                redirectURL = res['data']['instrumentResponse']['redirectInfo']
                cart_items.update(merchantTransactionId=res['data']['merchantTransactionId'])
                return redirect(redirectURL['url'])
        else:
            messages.error(request, "Payment request failed. Try Again")
            return redirect("cart:overview")
    return render(request, 'overview.html', context={"amountPayable" : amountPayable, 'address' : deliveryAddress,'cart_items' : cart_items, "pickUp" :pickUp})

def isPaymentRequest(merchantId, totalPayable):
    URL = PHONEPAY_URL
        
    merchantTransactionId = generate_merchant_transaction_id(merchantId)
    merchantUserId = generate_merchant_user_id(merchantId)
    data = {
        "merchantId": merchantId,
        "merchantTransactionId":merchantTransactionId,
        "merchantUserId":merchantUserId,
        "amount": int(totalPayable*100),
        "redirectUrl": "https://www.famousbookshop.in/order/successful/",
        "redirectMode": "POST",
        "callbackUrl": "https://www.famousbookshop.in/order/order-details/",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    # Convert the payload dictionary to a JSON string
    json_string = json.dumps(data)

    # Encode the JSON string to Base64
    encoded_data_bytes = base64.b64encode(json_string.encode('utf-8'))

    # Convert the bytes to a UTF-8 string
    encoded_data_str = encoded_data_bytes.decode('utf-8')
    print(PHONEPAY_SALT_KEY,"PHONEPAY_SALT_KEY")
    # Generate the X-VERIFY token
    hash_string = encoded_data_str + "/pg/v1/pay"+PHONEPAY_SALT_KEY
    # + "05992a0b-5254-4f37-86fb-e23bb79ea7e7"
    hashed_token = hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    payload = {
        "request" : encoded_data_str
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-VERIFY": "{}###1".format(hashed_token),
    }
    return requests.post(URL, json=payload, headers=headers)

def generate_merchant_transaction_id(merchant_id):
    unique_uuid = uuid.uuid4().hex[:36 - len(merchant_id) - 1]  # Subtract 1 for the underscore
    if Order.objects.filter(merchantTransactionId__iexact=unique_uuid).count() > 0:
        generate_merchant_transaction_id(merchant_id)
    else:
        merchant_transaction_id = f"{merchant_id}_{unique_uuid}"

    return merchant_transaction_id

def generate_merchant_user_id(merchant_id):
    unique_uuid = uuid.uuid4().hex[:30 - len(merchant_id) - 1]  # Subtract 1 for the underscore
    return f"{merchant_id}_{unique_uuid}"

def update_charge(request):
    if request.method=="POST":
        ch = request.POST.get("ch")
        cart_item = Cart.objects.filter(
            user=request.user).update(charges=ch)
        cart_item.filter(product__quantity__lte=0).delete()
        if  cart_item:
            return JsonResponse({'success': True, 'message': 'charges updated.'})
        else:
            return JsonResponse({'success': False, 'message': 'Something went wrong'})
    
# else:
#     return JsonResponse({'success': False, 'message': 'Request is tempored'})
"""
This function removes an item from the cart. If the user is authenticated, it deletes the item from the database. If not, it removes the item from the cookie.
"""
def remove_cart_item(request, cartId):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(id=cartId).delete()
            messages.success(request, "Cart item deleted")
            return redirect("cart:view_cart")
        except Cart.DoesNotExist:
            messages.error(request ,"Cart item not found")
            return redirect("cart:view_cart")
    else:
        cart_items = []
        cart_cookie = request.COOKIES.get('cart')

        if cart_cookie:
            cart_items = json.loads(cart_cookie)
        else:
            messages.error(request, "Add book to cart")
            return redirect("cart:view_cart")
        
        if cart_items:
            cart_items.remove(int(cartId))
            messages.success(request, "Cart item deleted")
            response = redirect("cart:view_cart")
            response.set_cookie('cart', json.dumps(cart_items))
            return response
        else:
            messages.error(request ,"Cart item not found")
            return redirect("cart:view_cart")
        
"""
This function updates the quantity of a book in the user's cart. It takes in a POST request containing the cart ID and the new quantity. If the user is authenticated, it updates the quantity of the book in the cart and returns a success message. If the user is not authenticated, it returns a failure message. If the request method is not POST, it returns a failure message. 
@param request - the POST request containing the cart ID and new quantity
@return a JSON response containing a success message and a message indicating whether the update was successful or not.
"""
def update_quantity(request):
    if request.method=="POST":
        cart_id = request.POST.get("cartId")
        qty = int(request.POST.get("qty"))
        if request.user.is_authenticated:
            cart_item = Cart.objects.get(id=int(cart_id))
            if cart_item.book.quantity:
                if qty > cart_item.book.quantity:
                    return JsonResponse({'success': False, 'message': 'Quantity must be below {}'.format(cart_item.book.quantity)})
                else:
                    cart = Cart.objects.filter(id=int(cart_id)).update(qty=qty)
                    cart.filter(product__quantity__lte=0).delete()
                    return JsonResponse({'success': True, 'message': 'Order qty updated.'})
            else:
                return JsonResponse({'success': False, 'message': 'Book is unavailable, please refresh the page.'})
        else:
            return JsonResponse({'success': False, 'message': 'Log in for qty update'})
    else:
        return JsonResponse({'success': False, 'message': 'Request is tempored'})
    
"""
This function adds an item to the user's wishlist and removes it from their cart.
@param request - the HTTP request object
@param itemId - the ID of the item to add to the wishlist
@return a redirect to the cart view page
"""
@login_required
def toWishList(request, itemId):
    getCart = Cart.objects.filter(id=int(itemId), user=request.user)
    getCart.filter(product__quantity__lte=0).delete()
    if getCart:
        Wishlist.objects.create(user=request.user, book=getCart[0].book)
        getCart.delete()
        messages.success(request, "Added book to wishlist")
        return redirect("cart:view_cart")
    messages.error(request, "Something went wrong")
    return redirect("cart:view_cart")