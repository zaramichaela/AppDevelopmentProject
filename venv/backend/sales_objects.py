import json
from datetime import date
import shelve
from backend import settings

#superclass for all sales objects
class sales_objects:
    #default init for creating a new object
    def __init__(self, UID,name, description, price, image_url):
        self.UID = UID #all item should have their unique UID
        #a string to be able to save to database shelve requirement
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url

    #for finding objects in shelves
    def set_UID(self, UID):
        self.UID = UID


    #convert to dictionary to store in shelve
    def serialize(self):
        if isinstance(self, date):
            serial = self.isoformat()
            return serial
        return self.__dict__


    #run this to update the database
    def save(self):
        s = shelve.open(settings.ITEMS_DB)
        try:
            print(self.UID)
            s[self.UID] = self.serialize()
            return True
        finally:
            s.close()
        return False

    def get_UID(self):
        return self.UID

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def get_image_url(self):
        return self.image_url

    def get_price(self):
        return self.price

    def subtract_sessions(self):
        pass

    def package_flag(self):
        return False


