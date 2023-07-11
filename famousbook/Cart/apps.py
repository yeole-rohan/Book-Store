from django.apps import AppConfig

class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cart'

    def ready(self):
        from .signals import merge_cart_items
