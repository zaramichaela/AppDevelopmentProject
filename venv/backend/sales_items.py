from backend.sales_objects import sales_objects 
import shelve
from backend import settings


class sales_items(sales_objects):

    #overwrite super for adding stocks to shop items
    def __init__(self, UID, name, description, price, image_url,stocks, discount, category):
        super().__init__(UID, name, description, price, image_url, discount)
        self.__stocks = stocks
        self.__category = category

    def get_stocks(self):
        return self.__stocks

    def set_stocks(self,stocks):
        self.__stocks = stocks

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.category = category

    def display_html(self):
        html = "testing"
        return html
