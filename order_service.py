import json

import requests
from cache import cache


class OrderService:
    __ORDER_SERVER_URLS = ["http://172.18.0.30:5000/", "http://172.18.0.31:5000/"]
    __PURCHASE_ENDPOINT = "purchase/{book_id}"

    def purchase(self, book_id):
        url_1 = self.__ORDER_SERVER_URLS[0] + self.__PURCHASE_ENDPOINT.format(book_id=book_id)
        url_2 = self.__ORDER_SERVER_URLS[1] + self.__PURCHASE_ENDPOINT.format(book_id=book_id)
        response = requests.post(url=url_1)
        if response.status_code >= 400:
            raise Exception("Failed to purchase book.")
        response = requests.post(url=url_2)
        if response.status_code >= 400:
            raise Exception("Failed to purchase book.")
        return json.loads(response.content)

    def get_url(self):
        current_server = cache.get("order_server")
        idx = current_server % 2
        cache.set("order_server", current_server + 1)
        return self.__ORDER_SERVER_URLS[idx]
