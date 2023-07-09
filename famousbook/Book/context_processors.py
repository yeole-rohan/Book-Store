import json
from .models import PrimaryCategory
from Cart.models import Cart
from Wishlist.models import Wishlist

"""
This function returns a dictionary containing the book categories, user cart, and wishlist. 
"""
def primaryCategory(request):
    bookCategory = list(PrimaryCategory.objects.all().values_list("name", flat=True))
    userCart = ''
    wishList = ''
    if request.user.id == None:
        cart_cookie = request.COOKIES.get('cart')
        if cart_cookie:
            userCart = json.loads(cart_cookie)
    else:
        userCart = list(Cart.objects.filter(
            user=request.user).values_list("book", flat=True))
        wishList = list(Wishlist.objects.filter(user=request.user).values_list("book", flat= True))
    return {"bookCategory" : bookCategory, 'userCart' : userCart, "wishList" : wishList}

# def wishCartCount(request):
#     return {"wishCount" : wishCount, "cartCount" : cartCount}