from backend.sales_objects import sales_objects
import shelve
from backend import settings


class sales_items(sales_objects):

    #overwrite super for adding stocks to shop items
    def __init__(self, UID, name, description, price, image_url,stocks):
        super().__init__(UID, name, description, price, image_url)
        self.stocks = stocks

    def get_stocks(self):
        return self.__stocks

    def set_stocks(self,stocks):
        self.__stocks = stocks

    def display_html(self):
        html = "testing"
        return html
