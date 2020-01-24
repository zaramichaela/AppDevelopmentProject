from datetime import date
import shelve
from backend import settings
import simplejson as jsons
import pickle

#superclass for all sales objects
class sales_objects(object):
    #default init for creating a new object
    def __init__(self, UID,name, description, price, image_url, discount):
        self.__UID = UID #all item should have their unique UID
        #a string to be able to save to database shelve requirement
        self.__name = name
        self.__description = description
        self.__price = price
        self.__image_url = image_url
        self.__available_flag = True
        self.__discount = discount

    #for finding objects in shelves
    def set_UID(self, UID):
        self.__UID = UID

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.discount = discount



    def price_before_discount(self):
        return self.__price

    def price_after_discount(self):
        return self.__price - ((self.__price/100) * self.__discount)

    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)


    #run this to update the database
    def save(self):
        s = shelve.open(settings.ITEMS_DB)
        try:
            s[self.__UID] = self.serialize()

            return True
        finally:
            s.close()
        return False

    def delete(self):
        s = shelve.open(settings.ITEMS_DB)
        try:
            del s[self.__UID]
            return True
        finally:
            s.close()
        return False


    def get_UID(self):
        return self.__UID

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def get_description(self):
        return self.__description

    def get_image_url(self):
        return self.__image_url

    def get_price(self):
        return self.__price

    def subtract_sessions(self):
        pass

    def package_flag(self):
        return False

    def get_available_flag(self):
        return self.__available_flag

    def set_available_flag(self, flag):
        self.__available_flag = flag
