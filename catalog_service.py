import requests
import json
from cache import cache


class CatalogService:
    __CATALOG_SERVER_URLS = ["http://172.18.0.20:5000/", "http://172.18.0.21:5000/"]
    __INFO_ENDPOINT = "info/{book_id}"
    __SEARCH_ENDPOINT = "search/{topic}"
    __UPDATE_QUANTITY_ENDPOINT = "update/{book_id}"

    def getBookInfo(self, book_id):
        # get book details from Catalog MS
        url = self.get_url() + self.__INFO_ENDPOINT.format(book_id=book_id)
        response = requests.get(url=url)
        if response.status_code >= 400:
            raise Exception("Failed to get book info.")
        return json.loads(response.content)

    def updateBookQuantity(self, book_id, quantity):
        # update quantity on catalog MS
        url = self.get_url() + self.__UPDATE_QUANTITY_ENDPOINT.format(book_id=book_id)
        response = requests.put(url=url, json={"quantity": quantity})
        if response.status_code >= 400:
            raise Exception("Failed to update book.")

    def searchBooks(self, topic):
        url = self.get_url() + self.__SEARCH_ENDPOINT.format(topic=topic)
        response = requests.get(url=url)
        if response.status_code >= 400:
            raise Exception("Failed to search topic.")
        return json.loads(response.content)

    def get_url(self):
        current_server = cache.get("catalog_server")
        if current_server is None:
            current_server = 0
        idx = current_server % 2
        cache.set("catalog_server", current_server + 1)
        return self.__CATALOG_SERVER_URLS[idx]
