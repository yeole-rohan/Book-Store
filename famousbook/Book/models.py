from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from User.models import User

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
        ('used-very-good', 'used very Good'),
        ('used-good', 'Used Good'),
        ('used-acceptable', 'Used Acceptable')
    )
    PRINT_BINDING = (
        ('paperback', 'Paperback'),
        ('hardcore', 'Hardcore')
    )
    LANGUAGE = (
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi')
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
    price = models.FloatField(_("MRP"),  default=0)
    bookImage = models.ImageField(_("Book Image"), upload_to="book-image/", default="", blank=True, null=True)
    bookURL = models.URLField(_("Book URL"), max_length=1000, default="", blank=True, null=True)
    isPublished = models.BooleanField(_("Published?"), default=False)
    isReturnable = models.BooleanField(_("Is Returnable"), default=False)
    isBestSell = models.BooleanField(_("Is Best Seller"), default=False)
    discountPrice = models.FloatField(_("Selling Price"), default=0, blank=True, null=True)
    author = models.TextField(_("Author List"), blank=True, null=True)
    bookBinding = models.CharField(_("Book Binding"),default="paperback", choices=PRINT_BINDING, max_length=100)
    bookCondition = models.CharField(_("Book Condition"), default="New", max_length=100)
    discountPercentage = models.PositiveIntegerField(_("Selling Percentage"), default=0, blank=True, null=True)
    description = models.TextField(_("Book Description"), default="", blank=True, null=True)
    bookLanguage = models.CharField(_("book Language"), choices=LANGUAGE, default="english", max_length=50)
    publisher = models.CharField(_("Book Pubisher"), max_length=500, default="", blank=True, null=True)
    readingAge = models.PositiveIntegerField(_("Reading Age"), default=0, blank=True, null=True)
    isbn = models.CharField(_("ISBN Number"), max_length=200, default="", blank=True, null=True)
    noOfPages = models.PositiveIntegerField(_("Number of Pages"), default=0, blank=True, null=True)
    publishedDate = models.CharField(_("Book Published Date"),max_length=200, blank=True, null=True)
    bookPrintedIn = models.CharField(_("Book Printed In"),choices=PRINTED_IN, default="india", max_length=50)
    bookSize = models.CharField(_("Book Size W*B*H in cm"), max_length=200, default="", blank=True, null=True)
    primaryCategory = models.ForeignKey("PrimaryCategory", verbose_name=_("Primary Category"), on_delete=models.CASCADE,  blank=True, null=True)
    secondaryCategory = models.ForeignKey("SecondaryCategory", verbose_name=_("Secondary Category"), on_delete=models.CASCADE, blank=True, null=True)
    book_position = models.CharField(_("book rack"), max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(_("Book Quantity"), default=0)
    book_type=models.CharField(_("Book Type"), choices=BOOK_TYPE, default="single", max_length=50)
    created = models.DateTimeField(_("Book created date"),auto_now_add=True)
    last_updated = models.DateTimeField(_("Book last updated"), auto_now=True)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        
        # save original values, when model is loaded from database,
        # in a separate attribute on the model
        instance._loaded_values = dict(zip(field_names, values))
        
        return instance
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        '''If price has change then update necessity fields'''
        if self.id is not None:
            if not self._state.adding:
                try:
                    print(self._loaded_values["price"], self.price, "self._loaded_values")
                    isPriceOrDiscountChanged = bool(self._loaded_values["price"] != self.price or self._loaded_values["discountPrice"] != self.discountPrice and self.discountPrice < self._loaded_values["price"])
                    print(isPriceOrDiscountChanged, "isPriceOrDiscountChanged")
                    if isPriceOrDiscountChanged and self.discountPrice:
                        self.discountPercentage = (float(self.price) - float(self.discountPrice)) / float(self.price)* 100
                except:
                    pass
                try:
                    isDiscountPercentageChanged = bool(self._loaded_values['discountPercentage'] != self.discountPercentage and self.discountPercentage < 100)
                    if isDiscountPercentageChanged and self.price:
                        self.discountPrice = float(self.price - (self.price*(self.discountPercentage/100)))
                except:
                    pass
              
        super(Book, self).save(*args, **kwargs)
        # calculate discount percentage at initial
        if not self.discountPercentage and self.price and self.discountPrice:
            self.discountPercentage = (float(self.price) - float(self.discountPrice)) / float(self.price)* 100
            self.save()

        # Calculate discount price by discount percentage and price
        if not self.discountPrice and self.discountPercentage and self.price:
            self.discountPrice = int(self.price - (self.price*(self.discountPercentage/100)))
            self.save()

        # Saves image from url
        if self.bookURL and not self.bookImage:
            # try:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.bookURL).read())
            img_temp.flush()
            self.bookImage.save(f"product_{self.pk}.png", File(img_temp))
            # except:
            #     print("URL dont have image ---- {}".format(self.bookURL))


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
    book_category = models.ForeignKey("PrimaryCategory", verbose_name=_("Book Category"), on_delete=models.CASCADE, default="")
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
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, blank=True, null=True)
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
    

class PinCodeStateCharges(models.Model):
    # Define the state code and full name as tuples
    STATE = (
        ("AN", "Andaman and Nicobar Islands"),
        ("AP", "Andhra Pradesh"),
        ("AR", "Arunachal Pradesh"),
        ("AS", "Assam"),
        ("BR", "Bihar"),
        ("CH", "Chandigarh"),
        ("CG", "Chhattisgarh"),
        ("DN", "Dadra and Nagar Haveli"),
        ("DD", "Daman and Diu"),
        ("DL", "Delhi"),
        ("GA", "Goa"),
        ("GJ", "Gujarat"),
        ("HR", "Haryana"),
        ("HP", "Himachal Pradesh"),
        ("JK", "Jammu and Kashmir"),
        ("JH", "Jharkhand"),
        ("KA", "Karnataka"),
        ("KL", "Kerala"),
        ("LA", "Ladakh"),
        ("MP", "Madhya Pradesh"),
        ("MH", "Maharashtra"),
        ("MN", "Manipur"),
        ("ML", "Meghalaya"),
        ("MZ", "Mizoram"),
        ("NL", "Nagaland"),
        ("OR", "Odisha"),
        ("PY", "Puducherry"),
        ("PB", "Punjab"),
        ("RJ", "Rajasthan"),
        ("SK", "Sikkim"),
        ("TN", "Tamil Nadu"),
        ("TS", "Telangana"),
        ("TR", "Tripura"),
        ("UP", "Uttar Pradesh"),
        ("UK", "Uttarakhand"),
        ("WB", "West Bengal"),
    )
    state = models.CharField(_("State"), choices=STATE,default="AN", max_length=100)
    initialCharge = models.PositiveIntegerField(_("Initial Charge"), default=100)
    threeBookCharge = models.PositiveIntegerField(_("After 3 Books Charge"), default=30)
    sixBookCharge = models.PositiveIntegerField(_("After 6 Books Charge"), default=20)
    freeShippingOn = models.PositiveIntegerField(_("Free Shiping on Order"), default=600)
    dispatchTime = models.PositiveIntegerField(_("Dispatch Time"), default=2)
    deliveryEstimate = models.PositiveIntegerField(_("Delivery Time in Days"), default=5)
    created_date = models.DateTimeField(_("Created Time"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Pin Code State Charges")
        verbose_name_plural = _("Pin Code State Charges")

    def __str__(self):
        return self.state