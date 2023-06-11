from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    author = forms.CharField(label="Author List", max_length=500, required=False)
    primaryCategory = forms.CharField(label="Primary Category", max_length=500, required=False)
    secondaryCategory = forms.CharField(label="Secondary Category", max_length=500, required=False)

    class Meta:
        model = Book
        exclude = ("discountPercentage", "bookURL", "created", "last_updated")

# class BookEditForm(forms.ModelForm):
#     author = forms.CharField(label="Author List", max_length=500, required=False)
#     primaryCategory = forms.CharField(label="Primary Category", max_length=500, required=False)
#     secondaryCategory = forms.CharField(label="Secondary Category", max_length=500, required=False)
#     class Meta:
#         model = Book
#         fields = ("",)
#         exclude = ("discountPercentage", "bookURL", "created", "last_updated")

class SingleISBNForm(forms.Form):
    ISBN = forms.CharField(label="Enter ISBN Number", max_length=100, required=True, )

class BulkSheetForm(forms.Form):
    sheet = forms.FileField(label="xlsx Sheet", required=True)