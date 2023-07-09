# signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import json
from Book.models import Book
from .models import Cart

@receiver(user_logged_in)
def merge_cart_items(sender, user, request, **kwargs):
    print("Signal Called")
    cart_items = ''
    cart_cookie = request.COOKIES.get('cart')
    if cart_cookie:
        cart_items = json.loads(cart_cookie)
    if cart_items:
        for cart_item in cart_items:
            if not Cart.objects.filter(user=user, book=Book.objects.get(id=cart_item)).exists():
                Cart.objects.create(user=user, book=Book.objects.get(id=cart_item))
