import shelve
from backend import settings
from backend.sales_items import *
from backend.sales_entry import *
from backend.sales_services import *
from backend.sales_package import *
import jsons
import pickle

#class for creating objects using dictionary
#doesnt save
class sales_factory:
    def __init__(self):
        pass

    #create shop items
    #can be use to generate a new one or recreate from database
    #dictionary defined

      #e.g. {'UID':'2', 'name':'name', 'description':'description','price':1,'image_url':1, 'stocks':4}    def create_salesitems(self, dict):
    def create_item(self,dict):
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
    def create_service(self,dict):
        try:
            item = sales_services(dict["UID"],dict["name"], dict["description"], dict["price"], dict["image_url"])
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

    def deserialize(self, dict):
        try:
            return pickle.loads(dict)
        except:
            return None


    #return all items from item database
    def get_all_items(self):
        items = []
        s = shelve.open(settings.ITEMS_DB)
        try:
            for key in s:
                items.append(self.deserialize(s[key]))
        finally:
            s.close()
        print(items)
        return items

    # return all services from service database
    def get_all_services(self):
        items = []
        s = shelve.open(settings.SERVICES_DB)
        try:
            for key in s:
                items.append(self.deserialize(s[key]))
        finally:
            s.close()
        print(items)
        return items

    #return all packages from package database
    def get_all_packages(self):
        items = []
        s = shelve.open(settings.PACKAGES_DB)
        try:
            for key in s:
                items.append(self.deserialize(s[key]))
        finally:
            s.close()
        print(items)
        return items

    #get a item with the specific UID
    def get_items(self, UID):
        #get shop items with UID
        #if exists return.
        #if not, return None.
        item = None
        s = shelve.open(settings.ITEMS_DB)
        try:
            item = self.deserialize(s[UID])
        finally:
            s.close()
        return self.create_items(item)

    #get service with the UID
    def get_services(self, UID):
        #get shop services with UID
        #if exists return.
        #if not, return None.
        service = None
        s = shelve.open(settings.SERVICES_DB)
        try:
            service = self.deserialize(s[UID])
        finally:
            s.close()
        return self.create_services(service)

    #get the package with UID
    def get_package(self, UID):
        package = None
        s = shelve.open(settings.SERVICES_DB)
        try:
            package = self.deserialize(s[UID])
        finally:
            s.close()
        return self.create_package(package)

    #for buying a product. will add to a new database
    def buy_product(self, user, salesitem, quantity=1):
        #salesitem is a sales_object
        salesentry = sales_entry(sales_object=sales_entry, quantity=quantity)
        return salesentry

