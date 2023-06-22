"""
URL configuration for famousbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

"""
This code defines the URL patterns for a Django web application. 
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(("Book.urls", "book"), namespace="book")),
    path('pages/', include(("StaticPages.urls", "staticPages"), namespace="staticPages")),
    path('account/', include(("User.urls", "user"), namespace="user")),
    path('cart/', include(("Cart.urls", "cart"), namespace="cart")),
    path('wishlist/', include(("Wishlist.urls", "wishlist"), namespace="wishlist")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
This line of code sets the handler404 variable to the function redirect404 in the famousbook.views module. This is used to handle 404 errors in a web application.
"""
handler404 = "famousbook.views.redirect404"
