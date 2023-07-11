from django.apps import AppConfig

class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Book'

    def ready(self):
        from .signals import delete_book_author_image, delete_book_image, delete_testimonial_image, delete_bundle_image_image, delete_coupon_image_image, delete_promo_image_image
