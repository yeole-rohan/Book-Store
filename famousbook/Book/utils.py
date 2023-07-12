from bs4 import BeautifulSoup
from datetime import datetime
from .models import Book

def createBook(data, ISBN):
    title = data.get("title") if data.get("title") else ""
    description = data.get("description") if data.get("description") else ""
    publisher = ",".join(data.get("publishers")) if data.get("publishers") else ""
    cover = data.get("covers")[0] if data.get("covers") else ''
    number_of_pages = data.get("number_of_pages") if data.get("number_of_pages") else 0
    publish_date = data.get("publish_date") if data.get("publish_date") else ""
    # languages = data.get("languages")[0]["key"].split("/languages/").join("") if data.get("languages") else "eng"

    if title and not Book.objects.filter(isbn__iexact=ISBN).exists():
        Book.objects.create(title=title,description=description, publisher=publisher, bookURL="https://covers.openlibrary.org/b/id/{}-M.jpg".format(cover), noOfPages=number_of_pages, isbn=ISBN, publishedDate=publish_date, bookLanguage="english")
        return True
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