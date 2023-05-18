from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from Book.models import Book
from .models import Wishlist

'''Add Wishlist Ajax View'''
@login_required
def addToWishList(request):
    if request.method == "POST":
        bookId = request.POST.get("bookId")
        createWishlist = Wishlist.objects.create(book=get_object_or_404(Book, id=bookId), user=request.user)
        if createWishlist:
            return JsonResponse({"status": "ok", "wishCount": Wishlist.objects.filter(user=request.user).count()})
    else:
        return JsonResponse({"status": "error", "message" : "Error while saving"})
    return JsonResponse({"status": "error", "message" : "Login Required"})

'''User Wishlist View'''
@login_required
def home(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, template_name="wishlist.html", context={'wishlist' : wishlist})

'''Remove Wishlist Book'''
@login_required
def deleteWishListBook(request):
    if request.method == "POST":
        bookId = request.POST.get("bookId")
        deleteWishlist = Wishlist.objects.filter(book=bookId, user=request.user)
        if deleteWishlist:
            deleteWishlist.delete()
            messages.success(request, "Removed book from wishlist")
            return redirect("wishlist:home")
    messages.error(request, "Something went wrong")
    return redirect("wishlist:home")