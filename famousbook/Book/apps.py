from django.apps import AppConfig

class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Book'

    def ready(self):
        print("delete Signal ready called")
        from .signals import delete_image
