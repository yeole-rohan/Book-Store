from django.db import models
from django.utils.translation import gettext_lazy as _

class Book(models.Model):
    PRINT_CONDITION = (
        ('new', 'New'),
        ('like-new', 'Like New'),
        ('used-ver-good', 'used very Good'),
        ('used-good', 'Used Good'),
        ('used-acceptable', 'Used Acceptable')
    )
    PRINT_BINDING = (
        ('paperback', 'Paperback'),
        ('hardcore', 'Hardcore')
    )
    LANGUAGE = (
        ('english', 'English'),
        ('hindi', 'Hindi'),
        ('marathi', 'Marathi')
    )
    PRINTED_IN = (
        ('india', 'India'),
        ('uk', 'UK'),
        ('usa', 'USA'),
        ('china', 'China'),
        ('others', "Others")
    )
    title = models.CharField(_("Book Title"), max_length=500, default="")
    price = models.DecimalField(_("Price"), max_digits=4, decimal_places=2, default="")
    bookImage = models.ImageField(_("Book Image"), upload_to="book-images/", default="")
    bookURL = models.URLField(_("Book URL"), max_length=1000, default="")
    discountPrice = models.DecimalField(_("Discount Price"), default="", max_digits=4, decimal_places=2)
    author = models.TextField(_("Author List"))
    bookBinding = models.CharField(_("Book Binding"),default="paperback", choices=PRINT_BINDING, max_length=100)
    bookCondition = models.CharField(_("Book Condition"), choices=PRINT_CONDITION,default="new", max_length=100)
    discountPercentage = models.PositiveIntegerField(_("Discount Percentage"), default=0)
    description = models.TextField(_("Book Description"), default="")
    isReturnable = models.BooleanField(_("Is Returnable"), default=False)
    bookLanguage = models.CharField(_("book Language"), choices=LANGUAGE, default="english", max_length=50)
    publisher = models.CharField(_("Book Pubisher"), max_length=500, default="")
    readingAge = models.PositiveIntegerField(_("Reading Age"), default=0)
    isbn = models.CharField(_("ISBN Number"), max_length=200, default="")
    noOfPages = models.PositiveIntegerField(_("Number of Pages"), default=0)
    publishedDate = models.DateField(_("Book Published Date"), auto_now=False, auto_now_add=False)
    bookPrintedIn = models.CharField(_("Book Printed In"),choices=PRINTED_IN, default="india", max_length=50)
    bookSize = models.CharField(_("Book Size L*B*H in cm"), max_length=200, default="")
    primaryCategory = models.TextField(_("Primary Category"), default="")
    secondaryCategory = models.TextField(_("Primary Category"), default="")
    created = models.DateTimeField(_("Cart created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Cart last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title