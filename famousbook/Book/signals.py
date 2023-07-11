from django.db.models.signals import post_delete
from django.dispatch import receiver
from Book.models import Book

@receiver(post_delete, sender=Book)
def delete_image(sender, instance, **kwargs):
    print("delete Signal has called")
    # Delete the bookImage file when the model instance is deleted
    if instance.bookImage:
        instance.bookImage.delete(save=False)
