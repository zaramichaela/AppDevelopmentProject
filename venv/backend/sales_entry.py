from datetime import datetime
from backend import settings
import shelve
#class represents each sales item made
#if needed can have subclass
class sales_entry:
    def __init__(self,sales_object, quantity=1):
        self.sales_object = sales_object
        self.quantity = quantity
        self.total_price = quantity * sales_object.price_after_discount()



    def set_sales_object(self, sales_object):
        #list of items/service/package bought
        self.sales_object = sales_object

    def get_sales_object(self):
        return self.sales_object


    def get_total_price(self):
        return self.total_price
