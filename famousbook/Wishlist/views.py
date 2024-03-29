from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from Book.models import Book
from .models import Wishlist
from Cart.models import Cart

'''Add Wishlist Ajax View'''
def addToWishList(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            bookId = request.POST.get("bookId")
            createWishlist, created = Wishlist.objects.get_or_create(book=get_object_or_404(Book, id=bookId), user=request.user)
            if not created:
                return JsonResponse({'success': False, 'message': 'Book is already in your wishlist.'})
            return JsonResponse({"success": True, "message" : "Added to wishlist", "wishCount": Wishlist.objects.filter(user=request.user).count()})
        else:
            return JsonResponse({"success": False, "message" : "Error while saving"})
    else:
       return JsonResponse({"success": False, "message" : "Login to add wishlist"}) 
'''User Wishlist View'''
@login_required
def home(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    try:
        featuredBooks = Book.objects.filter(isPublished=True, quantity__gt=0)[:10]
    except:
        featuredBooks = Book.objects.filter(isPublished=True, quantity__gt=0)
    try:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True, quantity__gt=0)[:10]
    except:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True, quantity__gt=0)
    history_books = []
    history = request.COOKIES.get('history')
    if history:
        history = json.loads(history)
        history_books = Book.objects.filter(isPublished=True, id__in=history, quantity__gt=0)
    return render(request, template_name="wishlist.html", context={'bestSeller':bestSeller, 'wishlist' : wishlist, 'history_books' :history_books, 'featuredBooks' : featuredBooks})

'''Remove Wishlist Book'''
@login_required
def deleteWishListBook(request, id):
    deleteWishlist = Wishlist.objects.filter(id=int(id), user=request.user)
    if deleteWishlist:
        deleteWishlist.delete()
        messages.success(request, "Removed book from wishlist")
        return redirect("wishlist:home")
    messages.error(request, "Something went wrong")
    return redirect("wishlist:home")

"""
This function takes a request and an item ID as input. It then retrieves the Wishlist object with the given ID and user. If the object exists, it creates a new Cart object with the user and book from the Wishlist object, deletes the Wishlist object, and returns a success message. If the Wishlist object does not exist, it returns an error message. 
@param request - the HTTP request object
@param itemId - the ID of the Wishlist object to be converted to a Cart object
@return a redirect to the wishlist home page
"""
@login_required
def toCart(request, itemId):
    getWish = Wishlist.objects.filter(id=int(itemId), user=request.user)
    if getWish:
        Cart.objects.create(user=request.user, book=getWish[0].book)
        getWish.delete()
        messages.success(request, "Added book to cart")
        return redirect("wishlist:home")
    messages.error(request, "Something went wrong")
    return redirect("wishlist:home")