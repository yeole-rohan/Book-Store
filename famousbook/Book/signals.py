from django.db.models.signals import post_delete
from django.dispatch import receiver
from Book.models import Book, BookAuthor, Testimonials, BundleBook, PromoBanner, CouponCode

@receiver(post_delete, sender=Book)
def delete_book_image(sender, instance, **kwargs):
    # Delete the bookImage file when the model instance is deleted
    if instance.bookImage:
        instance.bookImage.delete(save=False)

@receiver(post_delete, sender=BookAuthor)
def delete_book_author_image(sender, instance, **kwargs):
    # Delete the profile file when the model instance is deleted
    if instance.profile:
        instance.profile.delete(save=False)

@receiver(post_delete, sender=Testimonials)
def delete_testimonial_image(sender, instance, **kwargs):
    # Delete the testimonial_image file when the model instance is deleted
    if instance.testimonial_image:
        instance.testimonial_image.delete(save=False)

@receiver(post_delete, sender=BundleBook)
def delete_bundle_image_image(sender, instance, **kwargs):
    # Delete the image file when the model instance is deleted
    if instance.image:
        instance.image.delete(save=False)

@receiver(post_delete, sender=PromoBanner)
def delete_promo_image_image(sender, instance, **kwargs):
    # Delete the desktop_banner, mobile_bannner file when the model instance is deleted
    if instance.desktop_banner:
        instance.desktop_banner.delete(save=False)
    if instance.mobile_bannner:
        instance.mobile_bannner.delete(save=False)

@receiver(post_delete, sender=CouponCode)
def delete_coupon_image_image(sender, instance, **kwargs):
    # Delete the coupon_image file when the model instance is deleted
    if instance.coupon_image:
        instance.coupon_image.delete(save=False)