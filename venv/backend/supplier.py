
import shelve
from backend import settings
import pickle

class suppliers(object):

    #overwrite super for adding stocks to shop items
    def __init__(self, UID,name, address, phone_num,product, p_UID,  price):
        self.__UID = UID
        self.__name = name
        self.__address = address
        self.__phone_num = phone_num
        self.__pUID = p_UID
        self.__product = product
        self.__price = price


    def get_UID(self):
        return self.__UID

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_phone_num(self):
        return self.__phone_num

    def get_product(self):
        return self.__product

    def get_price(self):
        return self.__price

    def set_UID(self, UID):
        self.__UID = UID

    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def set_phone_num(self, phone_num):
        self.__phone_num = phone_num

    def set_product(self,product):
        self.__product = product

    def set_price(self, price):
        self.__price = price

    def save(self):
       s = shelve.open(settings.SUPPLIERS_DB)
       try:
            s[self.__UID] = self.serialize()
            return True
       finally:
            s.close()
       return False


    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)


    def get_pUID(self):
        return self.__pUID
