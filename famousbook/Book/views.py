from django.shortcuts import render
from django.db.models import Q
from .models import Book
from .forms import BookForm

def home(request):
    books = Book.objects.all()
    return render(request, template_name="home.html", context={'books':books})

# def bookSearch(request):
#     priceMin, priceMax = 0, 50000
#     discountMin, discountMax = 0, 100
#     if request.method == "POST":
#         keyword = 

def bookCategory(request, category):
    books = Book.objects.filter(Q(primaryCategory__icontains=category)|Q( secondaryCategory__icontains=category)).order_by("-created")
    priceMin, priceMax = 0, 50000
    discountMin, discountMax = 0, 100
    language, binding = '', ''
    # if request.method == "POST":
    #     keyword = 
    return render(request, template_name="categoryBooks.html", context={'books':books})