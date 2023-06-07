from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import requests
from .models import Book
from .utils import createBook
from .forms import BookForm, SingleISBNForm

isbns=[
9781421501246,
9781591168751,
9781421577791,
9781421590158,
9781787731721,
9781421599441,
9781974700394,
9781974704514,
9781421539652,
9781974703654,
9781974703661,
9781421539683]

def home(request):
    books = Book.objects.all()
    return render(request, template_name="home.html", context={'books':books, 'html' : 'html'})

# def bookSearch(request):
#     priceMin, priceMax = 0, 50000
#     discountMin, discountMax = 0, 100
#     if request.method == "POST":
#         keyword = 

def findBookSingleISBN(request):
    singleISBNForm = SingleISBNForm()
    
    if request.method == "POST":
        singleISBNForm = SingleISBNForm(request.POST or None)
        if singleISBNForm.is_valid():
            ISBN = request.POST.get("ISBN")
            # Fetch book from bookswagon
            data = requests.get('https://www.bookswagon.com/search-books/{}'.format(ISBN))
            # Function to validate, save book data
            status = createBook(data, ISBN)

            if status:
                messages.success(request, "Book Entry Added")

            if not status:
                messages.error(request, "Book Entry Failed")
            return redirect("book:findBookSingleISBN")
        else:
            print(singleISBNForm.errors)
    return render(request, template_name="single-isbn.html", context={'form' : singleISBNForm})

def bulkISBNUpload(request):
    errorISBNumber = []
    # if not status:
    #     errorISBNumber.append(ISBN)
    return render(request, template_name="bulk-isbn.html", context={})

def manualBookCreate(request):
    bookForm = BookForm()
    
    if request.method == "POST":
        bookForm = BookForm(request.POST or None, request.FILES or None)
        if bookForm.is_valid():
            bookForm.save()
            return redirect("book:manualBookCreate")
        else:
            print(bookForm.errors)
    return render(request, template_name="manual-book-create.html", context={'form' : bookForm})

def bulkSheetUpload(request):
    return render(request, template_name="bulk-sheet-upload.html", context={})


def bookDetails(request):
    return render(request, template_name="details.html", context={})

def bookCategory(request, category):
    books = Book.objects.filter(Q(primaryCategory__icontains=category)|Q( secondaryCategory__icontains=category)).order_by("-created")
    priceMin, priceMax = 0, 50000
    discountMin, discountMax = 0, 100
    language, binding = '', ''
    # if request.method == "POST":
    #     keyword = 
    return render(request, template_name="categoryBooks.html", context={'books':books})