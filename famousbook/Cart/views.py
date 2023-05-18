from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from Book.models import Book
from .models import Cart

'''Ajax View for adding to cart'''
def addToCart(request):
    '''Need Code update for logged in user'''
    if request.method == "POST":
        bookId = request.POST.get("bookId")
        if request.user.is_authenticated:
            if request.COOKIES.get('book'):
                pass
            createCart = Cart.objects.create(book=get_object_or_404(Book, id=bookId))
            if createCart:
                return JsonResponse({"status": "ok", "cartBookCount": Cart.objects.count()})
        else:
            if request.COOKIES.get('book'):
                bookCookieValue = request.COOKIES.get('book')
                response = JsonResponse({"status": "ok"}).set_cookie("book", bookCookieValue + bookId)
                return response({"cartBookCount": len(request.COOKIES['book'])})
            else:
                response = JsonResponse({"status": "ok"}).set_cookie("book", bookId)
                return response({"cartBookCount": len(request.COOKIES['book'])})
                
    return JsonResponse({"status": "error"})

