from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','price','bookImage','bookURL','discountPrice','author',
    'bookBinding','bookCondition','discountPercentage','description','isReturnable','bookLanguage','publisher','readingAge','isbn','noOfPages','publishedDate', 'bookPrintedIn', 'bookSize', 'primaryCategory', 'secondaryCategory', 'created', 'last_updated')