from django.http import JsonResponse
from django.contrib import messages
from Book.models import Book
import json, datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, CouponCode
from Order.models import Order
from Wishlist.models import Wishlist
from User.models import DeliveryAddress
from .forms import PromoCodeForm, DeliveryAddressForm, ShippingChargesForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from famousbook.settings import EMAIL_HOST_USER as EMAIL_USER

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
            
            return JsonResponse({'success': True, 'message': 'Book added to cart.', "cartCount" : Cart.objects.filter(user=request.user).count()})
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
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True)[:10]
    except:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True)
    try:
        featuredBooks = Book.objects.all()[:10]
    except:
        featuredBooks = Book.objects.all()
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        wish_items = Wishlist.objects.filter(user=request.user)
        amountPayable = paymentCost(cart_items)
        if request.method == "POST" and "coupon" in request.POST:
            promoCodeForm = PromoCodeForm(request.POST or None)
            if promoCodeForm.is_valid():
                code = request.POST.get('promoCode')
                # private Coupon Code
                if CouponCode.objects.filter(user=request.user, coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now()).exists():
                    coupon = CouponCode.objects.get(user=request.user, coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now())
                    Cart.objects.filter(user=request.user).update(coupon_code=coupon)
                    amountPayable = paymentCost(cart_items)
                elif CouponCode.objects.filter(coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now()).exists():
                    coupon = CouponCode.objects.get(coupon_code__iexact=code, expiry_time__gte=datetime.datetime.now())
                    Cart.objects.filter(user=request.user).update(coupon_code=coupon)
                    amountPayable = paymentCost(cart_items)
                else:
                    messages.error(request, "Promocode is expired.")
    elif 'cart' in request.COOKIES:
        cart_cookie = request.COOKIES.get('cart')
        print(cart_cookie)
        if cart_cookie:
            cart_ids = json.loads(cart_cookie)
            print("cart_ids", cart_ids)
            cart_items = Book.objects.filter(isPublished=True, id__in=cart_ids)
            print(cart_items)
    return render(request, 'cart.html', context={'bestSeller':bestSeller, 'featuredBooks':featuredBooks,'cart_items': cart_items, 'wish_items' : wish_items, "amountPayable" : amountPayable, 'promoCodeForm' : promoCodeForm})

def paymentCost(cart_items):
    amountPayable = {}
    discount_percentage = list(cart_items.values_list("coupon_code__discount_percentage", flat=True))
    mrpTotal, discount, totalPayable, withOutDiscount, couponDiscount, mumbaiCharge, india, east, shippingAmount = 0, 0, 0, 0, 0, 0, 0, 0, 0
    isFree = False
    for item in cart_items:
        mrpTotal += item.book.price * item.qty
       
        if item.charges and not item.charges == "enquire":
            if item.charges == "40":
                mumbaiCharge = mumbaiCharge + 40
            if item.charges == "50":
                india = india + 50
            if item.charges == "70":
                east = east + 70
        if item.book.discountPrice:
            discount += item.book.discountPrice * item.qty
        else:
            withOutDiscount += mrpTotal
    totalPayable = discount + withOutDiscount
    if discount_percentage and not discount_percentage[0] == None:
        couponDiscount = round(totalPayable * float(discount_percentage[0]/100), 2)
        totalPayable -= couponDiscount
    charge = cart_items.first().charges if cart_items else 0
    
    if mrpTotal > 500 and charge == "40":
        isFree = True
        shippingAmount = 0
    elif cart_items and charge == "40":
        shippingAmount = mumbaiCharge
    
    if mrpTotal > 700 and charge == "50":
        isFree = True
        shippingAmount = 0
    elif cart_items and charge == "50":
        shippingAmount = india
    
    if mrpTotal > 1000 and charge == "70":
        isFree = True
        shippingAmount = 0
    elif cart_items and charge == "70":
        shippingAmount = east
    if cart_items and charge == "enquire":
        shippingAmount = 0
    cart_items.update(shippingCharge = int(shippingAmount))
    amountPayable['mrpTotal'] = mrpTotal
    amountPayable['totalDiscount'] = discount
    amountPayable['totalSaving'] = float(mrpTotal - discount) + couponDiscount
    amountPayable["couponDiscount"] = couponDiscount
    amountPayable['totalPayable'] = totalPayable + shippingAmount
    amountPayable["shippingAmount"] = shippingAmount
    amountPayable["isFree"] = isFree
    return amountPayable

@login_required
def selectAddress(request):
    cart_items = Cart.objects.filter(user=request.user)
    amountPayable = paymentCost(cart_items)
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
                Cart.objects.filter(user=request.user).update(
                    deliveryAddress=DeliveryAddress.objects.get(id=request.POST.get("address")))
            return redirect("cart:overview")
    return render(request, 'selectAddress.html', context={"amountPayable" : amountPayable, 'addressList' : addressList, 'deliveryAddressForm' :deliveryAddressForm})

@login_required
def overview(request):
    cart_items = Cart.objects.filter(user=request.user)
    amountPayable = paymentCost(cart_items)
    pickUp = cart_items.first().pickType
    deliveryAddress=DeliveryAddress.objects.get(id=list(cart_items.values_list("deliveryAddress", flat=True))[0])
    charge = cart_items.first().charges
    if charge:
        shippingChargesForm = ShippingChargesForm(initial={"charges" : "".join(charge)})
    else:
        shippingChargesForm = ShippingChargesForm()
    if request.method=="POST":
        idList = []
        for cart in cart_items:
            orderId = Order.objects.create(user=request.user, book=cart.book, qty=cart.qty,pickType=cart.pickType,deliveryAddress=cart.deliveryAddress,coupon_code=cart.coupon_code, charges=cart.charges, orderPlaced=True, shippingCharge=cart.shippingCharge)
            idList.append(orderId.id)
        messages.success(request, "Your order has been placed.")
        subject = "Order Confirmation"
        loginHTMLTemplate = render_to_string("email-template/order.html", context={"orderList" : Order.objects.filter(id__in=idList).order_by("-created") }, )
        body = strip_tags(loginHTMLTemplate)
        send_mail(subject, body, EMAIL_USER, [request.user.email], html_message=loginHTMLTemplate)
        send_mail(subject, body, EMAIL_USER, [EMAIL_USER], html_message=loginHTMLTemplate)
        cart_items.delete()
        return redirect("order:myOrders")

    return render(request, 'overview.html', context={"amountPayable" : amountPayable, 'address' : deliveryAddress,'cart_items' : cart_items, "shippingChargesForm" : shippingChargesForm, "pickUp" :pickUp})

def update_charge(request):
    if request.method=="POST":
        ch = request.POST.get("ch")
        cart_item = Cart.objects.filter(
            user=request.user).update(charges=ch)
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
            if qty > cart_item.book.quantity:
                return JsonResponse({'success': False, 'message': 'Quantity must be below {}'.format(cart_item.book.quantity)})
            else:
                Cart.objects.filter(id=int(cart_id)).update(qty=qty)
                return JsonResponse({'success': True, 'message': 'Book qty updated.'})
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
    if getCart:
        Wishlist.objects.create(user=request.user, book=getCart[0].book)
        getCart.delete()
        messages.success(request, "Added book to wishlist")
        return redirect("cart:view_cart")
    messages.error(request, "Something went wrong")
    return redirect("cart:view_cart")