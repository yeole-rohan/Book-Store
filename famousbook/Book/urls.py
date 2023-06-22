from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("details/<str:id>/", views.bookDetails, name="bookDetails"),
    path("create/isbn/", views.findBookSingleISBN, name="findBookSingleISBN"),
    path("create/bulk/isbn", views.bulkISBNUpload, name="bulkISBNUpload"),
    path("create/book/", views.manualBookCreate, name="manualBookCreate"),
    path("create/book/sheet/", views.bulkSheetUpload, name="bulkSheetUpload"),
    path("inventory", views.inventory, name="inventory"),
    path("delete-single-book/<int:id>/", views.deleteSingleBook, name="deleteSingleBook"),
    path("edit-single-book/<int:id>/", views.editBook, name="editBook"),
    path("book/category/<str:category>/", views.bookCategory, name="bookCategory"),
    path("get/primary-category/ajax/<int:id>/", views.getBookPrimaryCategory, name="getBookPrimaryCategory"),
    path("suggestions/", views.bookSuggestions, name="bookSuggestions"),
    path("bundle-deals/<str:category>/", views.bundleDeals, name="bundleDeals"),
    path("offers/", views.offers, name="offers"),
]
