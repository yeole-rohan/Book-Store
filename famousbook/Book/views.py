from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import requests, csv, io, pandas, time, random, json
from datetime import datetime
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import Book, BookSelectedCategory, PrimaryCategory, SecondaryCategory, Testimonials, BookAuthor, BundleBook, CouponCode, PromoBanner
from .utils import createBook
from .forms import BookForm, SingleISBNForm, BulkSheetForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    try:
        featuredBooks = Book.objects.filter(isPublished=True)[:10]
    except:
        featuredBooks = Book.objects.filter(isPublished=True)
    try:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True)[:10]
    except:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True)
    testimonials = Testimonials.objects.all()
    authors = BookAuthor.objects.all()
    bundleBook = BundleBook.objects.all()
    primaryCategory = PrimaryCategory.objects.all()
    firstPromo = PromoBanner.objects.first()
    if firstPromo:
        otherPromo = PromoBanner.objects.all().exclude(id=firstPromo.id)
    else:
        otherPromo = ''
    return render(request, template_name="home.html", context={'featuredBooks':featuredBooks, 'testimonials' : testimonials, "authors" : authors, "bundleBook" :bundleBook, 'primaryCategory' :primaryCategory, 'otherPromo' : otherPromo, 'firstPromo' : firstPromo, "bestSeller" : bestSeller})

def allBooks(request):
    books = Book.objects.filter(isPublished=True).order_by("-created")
    bookLanguage = set(list(books.values_list("bookLanguage", flat=True)))
    primaryCategory = PrimaryCategory.objects.all()
    # Get the page from get request
    page = request.GET.get("page", 1)
    # set default, how many posts to appear in in single page
    paginator = Paginator(books, 60)

    # try to find next page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, template_name="all-books.html", context={'books':books, 'bookLanguage' : bookLanguage, 'primaryCategory' :primaryCategory})

def bundleDeals(request, category):
    books = Book.objects.filter(
        isPublished=True, primaryCategory__name__icontains=category, book_type="bundle").order_by("-created")
    return render(request, template_name="book-bundle.html", context={'books':books})

@login_required
def findBookSingleISBN(request):
    singleISBNForm = SingleISBNForm()
    
    if request.method == "POST":
        singleISBNForm = SingleISBNForm(request.POST or None)
        if singleISBNForm.is_valid():
            ISBN = request.POST.get("isbn")
            # Fetch book from bookswagon
            data = requests.get('https://openlibrary.org/isbn/{}.json'.format(int(ISBN)))
            if data:
                # Function to validate, save book data
                if not Book.objects.filter(isbn__iexact=ISBN).exists():
                    status = createBook(data.json(), ISBN)
                    if status:
                        messages.success(request, "Book Entry Added")
                        return redirect("book:findBookSingleISBN")
                    if not status:
                        messages.error(request, "Book Exist")
                else:
                    messages.error(request, "Book Exist")
                return redirect("book:findBookSingleISBN")
            else:
                messages.error(request, "Data is not available in API")
                return redirect("book:findBookSingleISBN")
        else:
            print(singleISBNForm.errors)
    return render(request, template_name="single-isbn.html", context={'form' : singleISBNForm})

@login_required
def bulkISBNUpload(request):
    bulkSheetForm = BulkSheetForm()
    failedISBN = []
    passedISBN = []
    if request.method == "POST":
        bulkSheetForm = BulkSheetForm(request.POST or None, request.FILES or None)
        if bulkSheetForm.is_valid():
            data = request.FILES['sheet']
            if not "xlsx" in data.name:
                messages.error(request, "Select xlsx file")
                return redirect("book:bulkSheetUpload")
            else:
                # Fetch book from bookswagon
                df = pandas.read_excel(data).fillna("")
                rows, column = df.shape
                bindingList = ['paperback', 'hardcore']
                # bookLanguageList = ['english', 'hindi', 'marathi']
                for index, row in df.iterrows():
                    # isbn = row.get('ISBN').replace(",", "")
                    print(row, "row")
                    if row.get('ISBN'):
                        isbn = row.get('ISBN').replace(",", "")
                        print(isbn, "isbn")
                        if not Book.objects.filter(isbn__iexact=isbn).exists():
                            # data = requests.get('https://www.bookswagon.com/search-books/{}'.format(row['ISBN']))
                            data = requests.get('https://openlibrary.org/isbn/{}.json'.format(int(isbn)))
                            
                            if data:
                                status = createBook(data.json(), isbn)
                                if not status:
                                    failedISBN.append(isbn)
                                else:
                                    passedISBN.append(isbn)
                            else:
                                failedISBN.append(isbn)
                            # Sleep for 4 sec if rows are more than 100
                            if rows >= 100:
                                time.sleep(4)
                        else:
                            failedISBN.append(isbn)
                    else:
                        messages.error(request, "Make sure ISBN is added as header to column.")
        else:
            print(bulkSheetForm.errors)
    return render(request, template_name="bulk-isbn-sheet-upload.html", context={'passedISBN':passedISBN, 'failedISBN':failedISBN, 'form' : bulkSheetForm})

@login_required
def manualBookCreate(request):
    bookForm = BookForm()
    
    if request.method == "POST":
        bookForm = BookForm(request.POST or None, request.FILES or None)
        if bookForm.is_valid():
            bookForm = bookForm.save(commit=False)
            discountPrice = request.POST.get("discountPrice")
            if discountPrice:
                bookForm.discountPercentage = (float(request.POST.get('price') - float(discountPrice))) / float(request.POST.get('price')) * 100
            bookForm.save()
            return redirect("book:manualBookCreate")
        else:
            print(bookForm.errors)
    return render(request, template_name="manual-book-create.html", context={'form' : bookForm})

@login_required
def bulkSheetUpload(request):
    bulkSheetForm = BulkSheetForm()
    if request.method == "POST":
        bulkSheetForm = BulkSheetForm(request.POST or None, request.FILES or None)
        if bulkSheetForm.is_valid():
            data = request.FILES['sheet']
            if not "xlsx" in data.name:
                messages.error(request, "Select xlsx file")
                return redirect("book:bulkSheetUpload")
            else:
                df = pandas.read_excel(data).fillna("")

                bindingList = ['paperback', 'hardcore']
                # bookLanguageList = ['english', 'hindi', 'marathi']
                for index, row in df.iterrows():
                    if PrimaryCategory.objects.filter(name=row.get('Primary Category')).exists():
                        primary = PrimaryCategory.objects.get(name=row.get('Primary Category'))
                        if SecondaryCategory.objects.filter(name=row.get('Secondary Category')).exists():
                            secondary = SecondaryCategory.objects.get(name=row.get('Secondary Category'))
                        else:
                            secondary = SecondaryCategory.objects.get(name="dc")
                    else:
                        primary = PrimaryCategory.objects.get(name="comic")
                    if not Book.objects.filter(isPublished=True, isbn__iexact=str(row['ISBN'])).exists():
                        book = Book.objects.create(title= row['Title'], bookURL=row['Image'], isbn=row['ISBN'], author=row['Author'], description=row['Description'] if row['Description'] else '', bookCondition =row['Condition'], price= int(row['MRP']) if row['MRP'] else 0, discountPrice=int(row['SP']) if row['SP'] else '', discountPercentage = (float(row['MRP']) - float(row['SP'])) / float(row['MRP']) * 100  if row['SP'] else '', quantity=int(row['Quantity']) if row['Quantity'] else 1, primaryCategory=primary, secondaryCategory=secondary, bookBinding= row['Format'].lower() if row['Format'].lower() in bindingList else 'paperback', bookLanguage='english',  noOfPages=int(row['Pages']), bookSize=row['Size'], )
                        book.save()
            
        else:
            print(bulkSheetForm.errors)
    return render(request, template_name="bulk-sheet-upload.html", context={'form' : bulkSheetForm})


def bookDetails(request, id):
    book = Book.objects.get(id=int(id))
    try:
        featuredBooks = Book.objects.all()[:10]
    except:
        featuredBooks = Book.objects.all()
    try:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True)[:10]
    except:
        bestSeller = Book.objects.filter(isPublished=True, isBestSell=True)
    book_items, history_books = [], []
    book_cookie = request.COOKIES.get('history')

    if book_cookie and not book_cookie ==None:
        book_items = json.loads(book_cookie)
    if not int(book.id) in book_items:
        book_items.append(book.id)
    history_books = Book.objects.filter(isPublished=True, id__in=book_items)
    similary_books = Book.objects.filter(Q(primaryCategory=book.primaryCategory) | Q(secondaryCategory=book.secondaryCategory), isPublished=True)
    response = render(request, template_name="details.html", context={'bestSeller':bestSeller,'featuredBooks':featuredBooks,'book' : book, 'history_books' : history_books, 'similary_books' : similary_books})
    response.set_cookie('history', json.dumps(book_items))
    return response

"""
Given a request and a category, retrieve all books that have the category as either their primary or secondary category and order them by creation date. Then render the book-category.html template with the retrieved books.
@param request - the request object
@param category - the category to filter books by
@return the rendered book-category.html template with the retrieved books
"""
def bookCategory(request, category):
    books = Book.objects.filter( Q(primaryCategory__name__icontains=category) | Q(secondaryCategory__name__icontains=category), isPublished=True).order_by("-created")
    secondryCategory = SecondaryCategory.objects.filter(primaryCategory__name__icontains=category)
    binding = set(list(books.values_list("bookBinding", flat=True)))
    bookLanguage = set(list(books.values_list("bookLanguage", flat=True)))

    # Get the page from get request
    page = request.GET.get("page", 1)
    # set default, how many posts to appear in in single page
    paginator = Paginator(books, 60)

    # try to find next page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, template_name="book-category.html", context={'books':books, 'category' : category, "secondryCategory" : secondryCategory, "binding" : binding, 'bookLanguage' : bookLanguage})

@login_required
def inventory(request):
    books = Book.objects.all()
    return render(request, template_name="inventory.html", context={'books':books})

@login_required
def editBook(request, id):
    if Book.objects.filter(isPublished=True, id=id).exists():
        book = Book.objects.get(id=id)
        bookForm = BookForm(instance=book)
    
        if request.method == "POST":
            bookForm = BookForm(request.POST or None, request.FILES or None, instance=book)
            if bookForm.is_valid():
                bookForm = bookForm.save(commit=False)
                discountPrice = request.POST.get("discountPrice")
                newImage = request.FILES.get('bookImage')
                if discountPrice:
                    bookForm.discountPercentage = (float(request.POST.get('price') - float(discountPrice))) / float(request.POST.get('price')) * 100
                if newImage:
                    bookForm.bookURL = ''
                bookForm.save()
                return redirect("book:manualBookCreate")
            else:
                print(bookForm.errors)
    else:
        book = ''
        messages.error(request, "Book not found")
        return redirect("book:inventory")
    return render(request, template_name="edit-book.html", context={'book':book, 'form' : bookForm})

@login_required
def deleteSingleBook(request, id):
    if Book.objects.filter(isPublished=True, id=id).exists():
        Book.objects.filter(isPublished=True, id=id).delete()
        messages.success(request, "Book deleted")
        return redirect("book:inventory")
    else:
        messages.error(request, "Book not found")
        return redirect("book:inventory")

def getBookPrimaryCategory(request, id):
    getPrimaryCategory = list(BookSelectedCategory.objects.filter(book=Book.objects.get(id=int(id))).values_list("book_category", flat=True))
    result = []
    labelDict = {}
    getAllCategories = PrimaryCategory.objects.all()
    for category in getAllCategories:
        if category.id in getPrimaryCategory:
            labelDict["id"] = category.id
            labelDict['text'] = category.name
            labelDict['selected'] = True
        else:
            labelDict["id"] = category.id
            labelDict['text'] = category.name
            labelDict['selected'] = False
        result.append(labelDict)
        labelDict = {}
    return JsonResponse({"status" : "ok", "label" : result})

"""
Given a request, return a list of book suggestions based on the keyword provided.
@param request - the request object
@return A JSON response containing the status and a list of book suggestions.
"""
def bookSuggestions(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")
        suggestions = list(Book.objects.filter( Q(title__icontains=keyword) | Q(author__icontains=keyword) | Q(publisher__icontains=keyword) | Q(isbn__icontains=keyword), isPublished=True).values_list("title", "id")) if keyword else ""

        return JsonResponse({'status':'ok', 'suggestions': suggestions})

def offers(request):
    offers = CouponCode.objects.filter(expiry_time__gte=datetime.today())
    return render(request, template_name="offers.html", context={'offers':offers})

def authorBooks(request, author):

    books = Book.objects.filter(
        isPublished=True, author__icontains=author).order_by("-created")

    # Get the page from get request
    page = request.GET.get("page", 1)
    # set default, how many posts to appear in in single page
    paginator = Paginator(books, 60)

    # try to find next page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, template_name="author-books.html", context={'books':books, 'author' : author})
def advanceSearch(request):
    result = []
    if request.method == "POST":
        categoryList = request.POST.get("categoryList[]") if request.POST.get("categoryList[]") else []
        binding = request.POST.get("binding[]") if request.POST.get("binding[]") else []
        language = request.POST.get("language[]") if request.POST.get("language[]") else []
        price = request.POST.getlist("price[]") if request.POST.get("price[]") else []
        discountPrice = request.POST.getlist("discountPrice[]") if request.POST.get("discountPrice[]") else []

        
        # Create a list to store the Q objects for price filtering
        price_query_list = []

        # Iterate over the price ranges
        for price_range in price:
            # Split the range into minimum and maximum values
            min_price, max_price = price_range.split('-')
            # Create a Q object to represent the range
            price_query = Q(price__range=(min_price, max_price))
            # Add the Q object to the list
            price_query_list.append(price_query)

        # Combine the Q objects for price filtering using OR operator
        combined_price_query = Q()
        for query in price_query_list:
            combined_price_query |= query

        # Create a list to store the Q objects for discount price filtering
        discount_price_query_list = []

        # Iterate over the discount price ranges
        for discount_price_range in discountPrice:
            # Split the range into minimum and maximum values
            min_discount_price, max_discount_price = discount_price_range.split('-')
            # Create a Q object to represent the range
            discount_price_query = Q(discountPrice__range=(min_discount_price, max_discount_price))
            # Add the Q object to the list
            discount_price_query_list.append(discount_price_query)

        # Combine the Q objects for discount price filtering using OR operator
        combined_discount_price_query = Q()
        for query in discount_price_query_list:
            combined_discount_price_query |= query
        # Filter the products based on price and discount price ranges
        bookList = Book.objects.filter( Q(primaryCategory__name__icontains=categoryList) | Q(secondaryCategory__name__icontains=categoryList) | Q(bookBinding__icontains=binding) | Q(bookLanguage__icontains=language), isPublished=True)
        # Remove duplicates from the query results
        bookList = bookList.distinct()
        if bookList:
            for book in bookList:
                result.append({
                    "id" : book.id,
                    "title" : book.title,
                    "author" : book.author,
                    "discountPercentage" : book.discountPercentage,
                    "description" : book.description,
                    "price" : book.price,
                    "bookURL" : book.bookURL,
                    "bookImage" : book.bookImage.url,
                    "discountPrice" :book.discountPrice
                })
            return JsonResponse({"success" : True, "bookList" : result, 'wishList' : [], 'userCart' : []})
        else:
            return JsonResponse({"success" : False, "message" : "No Result Found"})
    return JsonResponse({"success" : False, "message" : "No Result Found"})