import shelve
from backend import settings
from backend.sales_items import *
from backend.sales_objects import *
from backend.sales_entry import *
from backend.sales_services import *


#class for creating objects using dictionary
#doesnt save
class sales_factory:
    def __init__(self):
        pass

    #create shop items
    #can be use to generate a new one or recreate from database
    #dictionary defined

      #e.g. {'UID':'2', 'name':'name', 'description':'description','price':1,'image_url':1, 'stocks':4}    def create_salesitems(self, dict):
    def create_items(self,dict):
        try:
            item = sales_items(dict["UID"],dict["name"], dict["description"], dict["price"], dict["image_url"],dict["stocks"])
            return item
        except Exception as e:
            print(e)
            return None


    #create service items
    #can be use to generate a new one or recreate from database
    #dictionary defined
      #e.g. {'UID':'2', 'name':'name', 'description':'description','price':1,'image_url':1, 'datetime':datetime}
    def create_services(self,dict):
        try:
            item = sales_services(dict["UID"],dict["name"], dict["description"], dict["price"], dict["image_url"],dict["datetime"])
            return item
        except Exception as e:
            print(e)
            return None


    #create package items
    #can be use to generate a new one or recreate from database
    #dictionary defined
          #e.g. {'UID':'2', 'name':'name', 'description':'description','price':1,'image_url':1, 'expiry_duration':days, 'session':}
    def create_package(self, dict):
        try:
            item = shop_package(dict["UID"],dict["name"], dict["description"], dict["price"], dict["image_url"], dict["expiry_duration"],dict["sessions"],dict["remaining_sess"])
            return item
        except Exception as e:
            print(e)
            return None


    def get_all_items(self):
        items = []
        s = shelve.open(settings.ITEMS_DB)
        try:
            for key in s:
                items.append(self.create_items(s[key]))
        finally:
            s.close()
        print(items)
        return items


    def get_all_services(self):
        items = []
        s = shelve.open(settings.SERVICES_DB)
        try:
            for key in s:
                items.append(self.create_items(s[key]))
        finally:
            s.close()
        print(items)
        return items

    def get_all_package(self):
        items = []
        s = shelve.open(settings.PACKAGES_DB)
        try:
            for key in s:
                items.append(self.create_items(s[key]))
        finally:
            s.close()
        print(items)
        return items

    def get_all_items(self):
        items = []
        s = shelve.open(settings.SERVICES_DB)
        try:
            for key in s:
                items.append(self.create_items(s[key]))
        finally:
            s.close()
        print(items)
        return items


    def get_items(self, UID):
        #get shop items with UID
        #if exists return.
        #if not, return None.
        item = None
        s = shelve.open(settings.ITEMS_DB)
        try:
            item = s[UID]
        finally:
            s.close()
        return self.create_items(item)


    def get_services(self, UID):
        #get shop services with UID
        #if exists return.
        #if not, return None.
        service = None
        s = shelve.open(settings.SERVICES_DB)
        try:
            service = s[UID]
        finally:
            s.close()
        return self.create_services(service)

    def get_package(self, UID):
        package = None
        s = shelve.open(settings.SERVICES_DB)
        try:
            package = s[UID]
        finally:
            s.close()
        return self.create_package(package)

    #salesitem is a sales_object
    def buy_product(self, user, salesitem, quantity=1):
        salesentry = sales_entry(sales_object=sales_entry, quantity=quantity)
        salesentry.save()

    def check_UID(self):
