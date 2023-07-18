from bs4 import BeautifulSoup
from datetime import datetime
from .models import Book, PrimaryCategory

def createBook(data, ISBN):
    volumeInfo = data.get('volumeInfo')
    if volumeInfo:
        title = volumeInfo.get("title") if volumeInfo.get("title") else ""
        description = volumeInfo.get("description") if volumeInfo.get("description") else ""
        publisher = volumeInfo.get("publishers") if volumeInfo.get("publishers") else ""
        cover = volumeInfo.get("imageLinks")['thumbnail'] if volumeInfo.get("imageLinks") else ''
        number_of_pages = volumeInfo.get("pageCount") if volumeInfo.get("pageCount") else 0
        publish_date = volumeInfo.get("publishedDate") if volumeInfo.get("publishedDate") else ""
        language = data.get("language") if data.get("language") else "en"
        authors = ",".join(volumeInfo.get("authors")) if volumeInfo.get("authors") else ""
        publisher = volumeInfo.get("publisher") if volumeInfo.get("publisher") else ""
        category = volumeInfo.get("category")[0] if volumeInfo.get("category") else ""
        if PrimaryCategory.objects.filter(name=category).exists():
            primary = PrimaryCategory.objects.get(name=category)
        else:
            primary = None
        defaultLang = ['en','hi','mr']
        if title and not Book.objects.filter(isbn__iexact=ISBN).exists():
            Book.objects.create(title=title,description=description, publisher=publisher, bookURL=cover, noOfPages=number_of_pages, isbn=ISBN, bookLanguage=language if language in defaultLang else 'en', publishedDate=publish_date,author=authors, primaryCategory=primary)
            return True
        else:
            return False
    else:
        return False
 
# def createBook(data, isbn):
#     # try:
#     soup = BeautifulSoup(data.text, 'html.parser')
#     print(soup)
#     # title = soup.find(id="ctl00_phBody_ProductDetail_lblTitle").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblTitle") else ""
#     bookUrl = soup.find(id="ctl00_phBody_ProductDetail_imgProduct").get("src") if soup.find(id="ctl00_phBody_ProductDetail_imgProduct") else ""
#     author = soup.find(id="ctl00_phBody_ProductDetail_lblAuthor1").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblAuthor1") else ""
#     # publisher = soup.find(id="ctl00_phBody_ProductDetail_lblPublisher").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblPublisher") else ""
#     # binding = soup.find(id="ctl00_phBody_ProductDetail_lblBinding").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblBinding") else ""
#     # releasedDate = soup.find(id="ctl00_phBody_ProductDetail_lblRelease").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblRelease") else ""
#     discountPrice = soup.find(id="ctl00_phBody_ProductDetail_lblourPrice").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblourPrice") else ""
#     listPrice = soup.find(id="ctl00_phBody_ProductDetail_lblListPrice").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblListPrice") else ""
#     # shipping = soup.find(class_="available").get_text().strip() if soup.find(class_="available") else ""
#     about = soup.find(id="ctl00_phBody_ProductLongDesc_lblLongDesc").get_text().strip() if soup.find(id="ctl00_phBody_ProductLongDesc_lblLongDesc") else ""
#     print(soup.find_all("ISBN-13:"), "------details", soup.select("#bookdetail"), soup.select("#bookdetail li"))
#     otherData =  soup.find(id="bookdetail").find_all("li") if soup.find(id="bookdetail").find_all("li") else []
#     bookLanguage,noOfPages, width, height, breadth,publishedDate = '', '', '', '', '' ,''

#     for data in otherData:
#         print(data.get_text())
#         if "Language" in data.get_text().strip():
#             bookLanguage = data.get_text().split(":")[1].lower()
#         if "Pages" in data.get_text():
#             noOfPages = data.get_text().split(":")[1]
#         if "Date" in data.get_text():
#             publishedDate = data.get_text().split(":")[1]
#         if "Height" in data.get_text():
#             height = data.get_text().split(":")[1]
#         if "Series Title" in data.get_text():
#             title = data.get_text().split(":")[1]
#         if "Width" in data.get_text():
#             width = data.get_text().split(":")[1]
#         if "Binding" in data.get_text():
#             binding = data.get_text().split(":")[1]
#         if "Weight" in data.get_text():
#             height = data.get_text().split(":")[1]
#         if "Publisher" in data.get_text():
#             publisher = data.get_text().split(":")[1]
        
#     print()

#     bookSize = width + "*" + breadth + "*" + height
#     price= float(listPrice.replace("₹", "").replace(",", "."))
#     discountPrice = float(discountPrice.replace("₹", "").replace(",", "."))
#     print(title, price,discountPrice,author, binding, about,bookLanguage,bookUrl,noOfPages,bookLanguage, publisher, isbn,int(noOfPages),bookSize, publishedDate, (float(price) - float(discountPrice)) / float(price)* 100,width, height, breadth, '\n\n\n')
#     bindingList = ['paperback', 'hardcore']
#     bookLanguageList = ['english', 'hindi', 'marathi']
#     if title:
#         book = Book.objects.create(title= title.strip(), price= price, discountPrice=discountPrice,author=author.strip(), bookBinding= binding.lower() if binding.lower() in bindingList else 'paperback', description=about.strip(), bookURL=bookUrl, bookLanguage=bookLanguage.strip() if bookLanguage.strip() in bookLanguageList else 'english', publisher=publisher.strip(), isbn=isbn, noOfPages=int(noOfPages), bookSize=bookSize, publishedDate=datetime.strptime(publishedDate.strip().replace(" ", "/"), '%d/%b/%Y').date() if publishedDate else '', discountPercentage = (float(price) - float(discountPrice)) / float(price)* 100)
#         book.save()
#         return True
#     else:
#         return False
#     # except:
#     #     return False