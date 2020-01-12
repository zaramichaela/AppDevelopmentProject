from backend.sales_factory import *
from backend.coupon_factory  import *
import os

sfactory = sales_factory()
cfactory = coupon_factory()

#keeps all items in memory
#for fast searching, requires more memory.

class items_controller:


    def __init__(self):
        #initiate and store all data into memory
        self.all_coupons = cfactory.get_all_coupons()
        self.all_items = sfactory.get_all_items()
        self.all_packages = sfactory.get_all_packages()
        self.all_services = sfactory.get_all_services()


    def get_coupon_by_UID(self, coupon_UID):
        #check and find 1 coupon with the coupon_UID
        #return None if more than 1 found
        #can be used to check or search
        for i in self.all_coupons:
            if(i.get_UID() == coupon_UID):
                return i
        return False

    def get_coupon_by_code(self, coupon_code):
        #check and find 1 coupon with the couponcode
        #return None if more than 1 found
        coupon_item = [items for items in self.all_coupons if items.couponcode == coupon_code]
        if(len(coupon_item) == 1):
            return coupon_item
        else:
            return False


    def get_item_by_UID(self, UID):
        #check and return 1 item finding via item_UID. if more than 1, return None.
        for i in self.all_items:
            if(i.get_UID() == UID):
                return i
        return None

    def get_service_by_UID(self, UID):
        #check and return 1 item finding via item_UID. if more than 1, return None.
        for i in self.all_services:
            if(i.get_UID() == UID):
                return i
        return None
    def get_package_by_UID(self, UID):
        #check and return 1 item finding via item_UID. if more than 1, return None.
        for i in self.all_packages:
            if(i.get_UID() == UID):
                return i
        return None


    def get_all_sales_items(self):
        return self.all_items

    def get_all_sales_services(self):
        return self.all_services

    def get_all_sales_packages(self):
        return self.all_packages

    def get_all_coupons(self):
        return self.all_coupons


    ####################################################
    ####################################################
    ### check if UID exists, if does, return False ####
    def sales_item_check(self, UID):
        for i in self.all_items:
            if UID == i.getUID():
                return False
        return True

    def remove_sales_item(self, item):
        if(not sfactory.delete_db_sales_item(item.get_UID())):
            return False
        return self.all_items.remove(item)

    def remove_sales_package(self, item):
        if(not sfactory.delete_db_sales_package(item.get_UID())):
            return False
        return self.all_packages.remove(item)

    def remove_sales_service(self, item):
        if(not sfactory.delete_db_service(item.get_UID())):
            return False
        return self.all_services.remove(item)

    def remove_sales_coupon(self, item):
        if(not cfactory.delete_db_coupon(item.get_UID())):
            return False
        return self.all_coupons.remove(item)



    ####################################################

    ###################################################
    ###create item via here and thus updating memory###
    ### this is done to remove the limitation of the###
    ### shelves being##################################
    ### ###############################################
    ### overwrites old UID ############################
    ###################################################




    def create_and_save_item(self, dict):
        #create and save item in database and current memory
        item = sfactory.create_item(dict)
        self.all_items.append(item)
        item.save()
        return item

    def create_and_save_package(self, dict):
        #create and save package in database and current memory
        package = sfactory.create_package(dict)
        package.save()
        self.all_packages.append(package)
        return package

    def create_and_save_service(self, dict):
        #create and save service in database and current memory
        service = sfactory.create_service(dict)
        service.save()
        self.all_services.append(service)
        return service



    def create_and_save_coupon(self, dict):
        #create and save coupon in database and current memory
        coupon = cfactory.create_coupon(dict)
        self.all_coupons.append(coupon)
        return coupon



