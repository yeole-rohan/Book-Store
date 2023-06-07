from bs4 import BeautifulSoup
from datetime import datetime
from .models import Book

def createBook(data, isbn):
    try:
        soup = BeautifulSoup(data.text, 'html.parser')
        title = soup.find(id="ctl00_phBody_ProductDetail_lblTitle").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblTitle").get_text().strip() else ""
        bookUrl = soup.find(id="ctl00_phBody_ProductDetail_imgProduct").get("src") if soup.find(id="ctl00_phBody_ProductDetail_imgProduct").get("src") else ""
        author = soup.find(id="ctl00_phBody_ProductDetail_lblAuthor1").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblAuthor1").get_text().strip() else ""
        publisher = soup.find(id="ctl00_phBody_ProductDetail_lblPublisher").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblPublisher").get_text().strip() else ""
        binding = soup.find(id="ctl00_phBody_ProductDetail_lblBinding").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblBinding").get_text().strip() else ""
        releasedDate = soup.find(id="ctl00_phBody_ProductDetail_lblRelease").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblRelease").get_text().strip() else ""
        discountPrice = soup.find(id="ctl00_phBody_ProductDetail_lblourPrice").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblourPrice").get_text().strip() else ""
        listPrice = soup.find(id="ctl00_phBody_ProductDetail_lblListPrice").get_text().strip() if soup.find(id="ctl00_phBody_ProductDetail_lblListPrice").get_text().strip() else ""
        shipping = soup.find(class_="available").get_text().strip() if soup.find(class_="available").get_text().strip() else ""
        about = soup.find(id="aboutbook").find(class_="col-sm-12").get_text().strip() if soup.find(id="aboutbook").find(class_="col-sm-12").get_text().strip() else ""
        otherData =  soup.find(id="bookdetail").find_all("li") if soup.find(id="bookdetail").find_all("li") else []
        bookLanguage,noOfPages, width, height, breadth,publishedDate = '', '', '', '', '' ,''

        for data in otherData:
            print(data.get_text())
            if "Language" in data.get_text().strip():
                bookLanguage = data.get_text().split(":")[1].lower()
            if "Pages" in data.get_text():
                noOfPages = data.get_text().split(":")[1]
            if "Date" in data.get_text():
                publishedDate = data.get_text().split(":")[1]
            if "Height" in data.get_text():
                height = data.get_text().split(":")[1]
            
            if "Width" in data.get_text():
                width = data.get_text().split(":")[1]
            if "Weight" in data.get_text():
                height = data.get_text().split(":")[1]
            
        print(bookLanguage,noOfPages, width, height, breadth, "0000000000000000000000000000")

        bookSize = width + " " + breadth + " " + height
        price= float(listPrice.replace("₹", "").replace(",", "."))
        discountPrice = float(discountPrice.replace("₹", "").replace(",", "."))
        print(price, discountPrice, "=======================")
        bindingList = ['paperback', 'hardcore']
        bookLanguageList = ['english', 'hindi', 'marathi']
        if title:
            book = Book.objects.create(title= title.strip(), price= price, discountPrice=discountPrice,author=author.strip(), bookBinding= binding.lower() if binding.lower() in bindingList else 'paperback', description=about.strip(), bookURL=bookUrl, bookLanguage=bookLanguage.strip() if bookLanguage.strip() in bookLanguageList else 'india', publisher=publisher.strip(), isbn=isbn, noOfPages=int(noOfPages), bookSize=bookSize, publishedDate=datetime.strptime(publishedDate.strip().replace(" ", "/"), '%d/%b/%Y').date() if publishedDate else '')
            book.save()
            return True
        else:
            return False
    except:
        return False