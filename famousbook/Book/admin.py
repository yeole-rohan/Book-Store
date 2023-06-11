from django.contrib import admin
from .models import Book, PrimaryCategory, SecondaryCategory

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','price','bookImage','bookURL','discountPrice','author',
    'bookBinding','bookCondition','discountPercentage','description','isReturnable','bookLanguage','publisher','readingAge','isbn','noOfPages','publishedDate', 'bookPrintedIn', 'bookSize', 'primaryCategory', 'secondaryCategory', 'created', 'last_updated')

@admin.register(PrimaryCategory)
class PrimaryCategoryAdmin(admin.ModelAdmin):
    list_display= ("id", "name", "image", "created", "last_updated")

@admin.register(SecondaryCategory)
class SecondaryCategoryAdmin(admin.ModelAdmin):
    list_display= ("id", "name", "primaryCategory", "created", "last_updated")
