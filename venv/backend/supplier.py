
import shelve
from backend import settings
import pickle

class suppliers():

    #overwrite super for adding stocks to shop items
    def __init__(self, UID,name, address, phone_num,product,  price):
        self.UID = UID
        self.name = name
        self.address = address
        self.phone_num = phone_num
        self.product = product
        self.price = price


    def get_UID(self):
        return self.UID

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_phone_num(self):
        return self.phone_num

    def get_product(self):
        return self.product

    def get_price(self):
        return self.price

    def set_UID(self, UID):
        self.UID = UID

    def set_name(self, name):
        self.name = name

    def set_address(self, address):
        self.address = address

    def set_phone_num(self):
        self.phone_num = phone_num

    def set_product(self,product):
        self.product = product

    def set_price(self, price):
        self.price = price

    def save(self):
       s = shelve.open(settings.SUPPLIERS_DB)
       try:
            s[self.UID] = self.serialize()
            return True
       finally:
            s.close()
       return False


    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)
