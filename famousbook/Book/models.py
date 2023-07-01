from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


class PrimaryCategory(models.Model):
    name = models.CharField(_("Primary Category"), max_length=100)
    image = models.ImageField(_("Image"), upload_to="category-image/", null=True)
    created = models.DateTimeField(_("Created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Primary Category")
        verbose_name_plural = _("Primary Categorys")

    def __str__(self):
        return self.name

class SecondaryCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    primaryCategory = models.ForeignKey("PrimaryCategory", verbose_name=_("Primary Category"), on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Secondary Category")
        verbose_name_plural = _("Secondary Categorys")

    def __str__(self):
        return self.name

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
    BOOK_TYPE = (
        ("single", "Single"),
        ("bundle", "Bundle")
    )
    title = models.CharField(_("Book Title"), max_length=500, blank=False, null=False)
    price = models.FloatField(_("Price"),  default=0)
    bookImage = models.ImageField(_("Book Image"), upload_to="book-image/", default="", blank=True, null=True)
    bookURL = models.URLField(_("Book URL"), max_length=1000, default="", blank=True, null=True)
    isPublished = models.BooleanField(_("Published?"), default=False)
    discountPrice = models.FloatField(_("Discount Price"), default=0, blank=True, null=True)
    author = models.TextField(_("Author List"), blank=True, null=True)
    bookBinding = models.CharField(_("Book Binding"),default="paperback", choices=PRINT_BINDING, max_length=100)
    bookCondition = models.CharField(_("Book Condition"), choices=PRINT_CONDITION,default="new", max_length=100)
    discountPercentage = models.PositiveIntegerField(_("Discount Percentage"), default=0, blank=True, null=True)
    description = models.TextField(_("Book Description"), default="", blank=True, null=True)
    isReturnable = models.BooleanField(_("Is Returnable"), default=False)
    bookLanguage = models.CharField(_("book Language"), choices=LANGUAGE, default="english", max_length=50)
    publisher = models.CharField(_("Book Pubisher"), max_length=500, default="", blank=True, null=True)
    readingAge = models.PositiveIntegerField(_("Reading Age"), default=0, blank=True, null=True)
    isbn = models.CharField(_("ISBN Number"), max_length=200, default="", blank=True, null=True)
    noOfPages = models.PositiveIntegerField(_("Number of Pages"), default=0, blank=True, null=True)
    publishedDate = models.DateField(_("Book Published Date"), blank=True, null=True)
    bookPrintedIn = models.CharField(_("Book Printed In"),choices=PRINTED_IN, default="india", max_length=50)
    bookSize = models.CharField(_("Book Size W*B*H in cm"), max_length=200, default="", blank=True, null=True)
    primaryCategory = models.ForeignKey("PrimaryCategory", verbose_name=_("Primary Category"), on_delete=models.CASCADE,  blank=True, null=True)
    secondaryCategory = models.ForeignKey("SecondaryCategory", verbose_name=_("Secondary Category"), on_delete=models.CASCADE, blank=True, null=True)
    book_position = models.CharField(_("book rack"), max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(_("Book Quantity"), default=1)
    book_type=models.CharField(_("Book Type"), choices=BOOK_TYPE, default="single", max_length=50)
    created = models.DateTimeField(_("Cart created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Cart last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Finds Book Percentage
        print(self.discountPrice, self.price, "save method")
        # if self.discountPrice:
        #     self.discountPercentage = 
        #     self.save()

        # Saves image from url
        if self.bookURL and not self.bookImage:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.bookURL).read())
            img_temp.flush()
            self.bookImage.save(f"product_{self.pk}.png", File(img_temp))


class BookAuthor(models.Model):
    name = models.CharField(_("Author Name"), max_length=200)
    profile = models.ImageField(_("Author Image"),  upload_to="author-images/", default="")
    created = models.DateTimeField(_("Created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Book Author")
        verbose_name_plural = _("Book Authors")

    def __str__(self):
        return self.name

class Testimonials(models.Model):
    testimonial_image = models.ImageField(_("Testimonial Image"), upload_to="testimonial-image/", default="")
    name = models.CharField(_("Name"), max_length=200)
    review = models.CharField(_("Review"), max_length=250)
    created = models.DateTimeField(_("Created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Last updated"), auto_now=True)
    rating = models.PositiveIntegerField(_("Rating"), help_text="1,2,3,4,5 any")
    class Meta:
        verbose_name = _("Testimonials")
        verbose_name_plural = _("Testimonials")

    def __str__(self):
        return self.name

class BookSelectedCategory(models.Model):
    book_category = models.ForeignKey("PrimaryCategory", verbose_name=_("Book Category"), on_delete=models.CASCADE)
    book = models.ForeignKey("Book", verbose_name=_("Book"), on_delete=models.CASCADE)
    created_date = models.DateTimeField(_("Created Time"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Updated"), auto_now=True)

class BundleBook(models.Model):
    book_category = models.ForeignKey("PrimaryCategory", verbose_name=_("Book Category"), on_delete=models.CASCADE)
    image = models.ImageField(_("Bundle Image"), upload_to="bundle-image/")
    created_date = models.DateTimeField(_("Created Time"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Updated"), auto_now=True)
    class Meta:
        verbose_name = _("Bundle Book")
        verbose_name_plural = _("Bundle Books")

    def __str__(self):
        return str(self.id)

class PromoBanner(models.Model):
    book_category = models.ForeignKey("PrimaryCategory", verbose_name=_("Book Category"), on_delete=models.CASCADE, blank=True, null=True)
    desktop_banner = models.ImageField(_("Desktop Banner"), upload_to="banner/")
    mobile_bannner = models.ImageField(_("Mobile Banner"), upload_to="banner/")
    created_date = models.DateTimeField(_("Created Time"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Updated"), auto_now=True)
    

    class Meta:
        verbose_name = _("Promo Banner")
        verbose_name_plural = _("Promo Banners")

    def __str__(self):
        return str(self.id)

class CouponCode(models.Model):
    coupon_image = models.ImageField(_("Coupon Code"), upload_to="coupen-image/", null=True)
    coupon_code = models.CharField(_("Coupon Code"), max_length=50)
    discount_percentage = models.PositiveIntegerField(_("Discount Percentage"), default=0)
    expiry_time = models.DateTimeField(_("Expiry Date Time"))
    details = models.TextField(_("Coupon Code Details"))
    created_date = models.DateTimeField(_("Created Time"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Updated"), auto_now=True)
    class Meta:
        verbose_name = _("Coupen Code")
        verbose_name_plural = _("Coupen Codes")

    def __str__(self):
        return self.coupon_code