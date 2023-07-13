from django.contrib import admin
from .models import Book, PrimaryCategory, SecondaryCategory, Testimonials, BookAuthor, BundleBook, CouponCode, PromoBanner



@admin.action(description="Duplicate selected record")
def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'quantity','isPublished','price','bookImage','bookURL','discountPrice','author', 'book_position','isBestSell', 'book_type',
    'bookBinding','bookCondition','discountPercentage','description','isReturnable','bookLanguage','publisher','readingAge','isbn','noOfPages','publishedDate', 'bookPrintedIn', 'bookSize', 'primaryCategory', 'secondaryCategory', 'created', 'last_updated')
    search_fields = ["book_position", 'title', 'primaryCategory__name', 'isbn', 'author']
    list_filter = ['isBestSell','isReturnable', 'isPublished']
    actions = [duplicate_event]
    



@admin.register(PrimaryCategory)
class PrimaryCategoryAdmin(admin.ModelAdmin):
    list_display= ("id", "name", "image", "created", "last_updated")

@admin.register(SecondaryCategory)
class SecondaryCategoryAdmin(admin.ModelAdmin):
    list_display= ("id", "name", "primaryCategory", "created", "last_updated")

@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display= ("id", "name", "review", "rating", "testimonial_image", "created", "last_updated")

@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "profile", "created", "last_updated")

@admin.register(BundleBook)
class BundleBookAdmin(admin.ModelAdmin):
    list_display = ("id", "book_category", "image", "created_date", "last_updated")

@admin.register(CouponCode)
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "coupon_image", "discount_percentage", "coupon_code", "expiry_time", "details", "created_date", "last_updated")

@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ("id", "book_category", "desktop_banner", "mobile_bannner", "created_date", "last_updated")
