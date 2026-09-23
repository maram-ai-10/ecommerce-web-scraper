import requests
from bs4 import BeautifulSoup
import pandas as pd

class BookItem:
    def __init__(self, title, price, availability):
        self.title = title
        self.price = price
        self.availability = availability

    def to_dict(self):
        return {
            "Title": self.title,
            "Price": self.price,
            "Availability": self.availability
        }

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.collected_data = []

    def fetch_data(self):
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            availability = book.find("p", class_="instock availability").text.strip()
            
            item = BookItem(title, price, availability)
            self.collected_data.append(item.to_dict())

    def export_to_excel(self, filename="books_data.xlsx"):
        if not self.collected_data:
            return
        df = pd.DataFrame(self.collected_data)
        df.to_excel(filename, index=False)

if __name__ == "__main__":
    target_url = "http://books.toscrape.com/"
    scraper = WebScraper(target_url)
    scraper.fetch_data()
    scraper.export_to_excel("products.xlsx")
