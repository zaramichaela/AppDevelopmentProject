from datetime import date
import shelve
from backend import settings
import simplejson as jsons
import pickle

#superclass for all sales objects
class sales_objects(object):
    #default init for creating a new object
    def __init__(self, UID,name, description, price, image_url):
        self._UID = UID #all item should have their unique UID
        #a string to be able to save to database shelve requirement
        self._name = name
        self._description = description
        self._price = price
        self._image_url = image_url
        self._available_flag = True

    #for finding objects in shelves
    def set_UID(self, UID):
        self._UID = UID


    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)


    #run this to update the database
    def save(self):
        s = shelve.open(settings.ITEMS_DB)
        try:
            s[self._UID] = self.serialize()

            return True
        finally:
            s.close()
        return False

    def delete(self):
        s = shelve.open(settings.ITEMS_DB)
        try:
            del s[self._UID]
            return True
        finally:
            s.close()
        return False


    def get_UID(self):
        return self._UID

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def set_description(self, description):
        self._description = description

    def get_description(self):
        return self._description

    def get_image_url(self):
        return self._image_url

    def get_price(self):
        return self._price

    def subtract_sessions(self):
        pass

    def package_flag(self):
        return False

    def get_available_flag(self):
        return self.available_flag

    def set_available_flag(self, flag):
        self.available_flag = flag
