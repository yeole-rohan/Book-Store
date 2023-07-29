from django.contrib import admin
from .models import Book, PrimaryCategory, SecondaryCategory, Testimonials, BookAuthor, BundleBook, CouponCode, PromoBanner, PinCodeStateCharges



@admin.action(description="Duplicate selected record")
def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','shortTitle', 'quantity','isPublished','price','bookImage','shortBookURL','discountPrice','shortAuthor', 'book_position','isBestSell', 'book_type',
    'bookBinding','bookCondition','discountPercentage','shortDescription','isReturnable','bookLanguage','publisher','readingAge','isbn','noOfPages','publishedDate', 'bookPrintedIn', 'bookSize', 'primaryCategory', 'secondaryCategory', 'created', 'last_updated')
    search_fields = ["book_position", 'title', 'primaryCategory__name', 'isbn', 'author']
    list_filter = ['isBestSell','isReturnable', 'isPublished']
    actions = [duplicate_event]
    
    # Create Short Descrption in admin column
    def shortDescription(self, obj):
        if obj.description:
            return obj.description[:10] + '...' if len(obj.description) > 10 else obj.description
    
    def shortBookURL(self, obj):
        if obj.bookURL:
            return obj.bookURL[:10] +'...' if len(obj.bookURL) > 10 else obj.bookURL
    
    def shortTitle(self, obj):
        if obj.title:
            return obj.title[:20] +'...' if len(obj.title) > 20 else obj.title
    
    def shortAuthor(self, obj):
        if obj.author:
            return obj.author[:20] +'...' if len(obj.author) > 20 else obj.author
    # Sets user friendly name to admin column
    shortDescription.short_description = 'description'
    shortBookURL.short_description = 'book url'
    shortTitle.short_description = 'title'

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

@admin.register(PinCodeStateCharges) 
class PinCodeStateChargesAdmin(admin.ModelAdmin):
    list_display = ('state', 'initialCharge', 'threeBookCharge', 'sixBookCharge', 'freeShippingOn', 'dispatchTime', 'deliveryEstimate', 'created_date', 'last_updated')
    list_filter = ('dispatchTime', 'deliveryEstimate')
    search_fields = ('state',)
    ordering = ('state',)