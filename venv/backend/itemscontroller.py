from backend.sales_factory import *
from backend.coupon_factory import *
from backend.sales_receipt import *
from backend.sales_entry import *
from backend.appointment import *
import os
import uuid
from random import randint

####################################################################################
sfactory = sales_factory()
cfactory = coupon_factory()
####################################################################################

#keeps all items in memory
#for fast searching, requires more memory.

####################################################################################
class items_controller:
    def __init__(self):
        #initiate and store all data into memory
        self.__all_coupons = cfactory.get_all_coupons_db()
        self.__all_items = sfactory.get_all_items_db()
        self.__all_packages = sfactory.get_all_packages_db()
        self.__all_services = sfactory.get_all_services_db()
        self.__all_appointment = get_all_appointments()
        self.__all_receipt = sfactory.get_all_receipt_db()
        self.arrange_appointments()

    def arrange_appointments(self):
        self.__all_appointment = sorted(self.__all_appointment, key=lambda object1: object1.date)

    def get_coupon_by_UID(self, coupon_UID):
        #check and find 1 coupon with the coupon_UID
        #return None if more than 1 found
        #can be used to check or search
        #loop through the list of all coupons
        for i in self.__all_coupons:
            #if item UID equals to the parameter UID return the item
            if(i.get_UID() == coupon_UID):
                return i
        #return False if no item found
        return False


    def get_coupon_by_code(self, coupon_code):
        #check and find 1 coupon with the couponcode
        #return None if more than 1 found
        for i in self.__all_coupons:
            if(i.get_couponcode() == coupon_code):
                return i
        return False

    def get_item_by_UID(self, UID):
        #check and return 1 item finding via item_UID. if more than 1, return None.
        for i in self.__all_items:
            if(i.get_UID() == UID):
                return i
        return None


    def get_service_by_UID(self, UID):
        #check and return 1 item finding via item_UID. if more than 1, return None.
        for i in self.__all_services:
            if(i.get_UID() == UID):
                return i
        return None


    def get_package_by_UID(self, UID):
        #check and return 1 item finding via package_UID. if more than 1, return None.
        for i in self.__all_packages:
            if(i.get_UID() == UID):
                return i
        return None


    def get_suppliers_by_UID(self, UID):
        #check and return 1 item finding via suppliers_UID. if more than 1, return None.
        for i in self.__all_suppliers:
            if(i.get_UID() == UID):
                return i
        return None


    def get_receipt_by_UID(self, UID):
        #check and return 1 item finding via suppliers_UID. if more than 1, return None.
        for i in self.__all_receipt:
            if(i.get_UID() == UID):
                return i
        return None

    def get_receipt_by_user(self, username):
        #check and return 1 item finding via suppliers_UID. if more than 1, return None.
        list1 = sorted(self.__all_receipt, key=lambda receipt: receipt.sales_datetime, reverse=True)
        for i in self.__all_receipt:
            if(i.get_username() == username):
                return i
        return None

    def get_all_sales_items(self):
        #returns current items lists.
        return self.__all_items


    def get_all_sales_services(self):
        #returns current services lists.
        return self.__all_services


    def get_all_sales_packages(self):
        #returns current packages lists.
        return self.__all_packages


    def get_all_coupons(self):
        #returns current coupon lists.
        return self.__all_coupons

    ####################################################
    ####################################################
    ### check if UID exists, if does, return False ####
    ###################################################
    ###################################################

    def sales_item_check(self, UID):
        for i in self.__all_items:
            if UID == i.getUID():
                return False
        return True


    def remove_sales_item(self, item):
        flag = sfactory.delete_db_sales_item(item.get_UID())
        if(flag):
            self.__all_items.remove(item)
            return True
        return False


    def remove_sales_package(self, item):
        if(not sfactory.delete_db_sales_package(item.get_UID())):
            return False
        self.__all_packages.remove(item)
        return True


    def remove_sales_service(self, item):
        if(not sfactory.delete_db_service(item.get_UID())):
            return False
        self.__all_services.remove(item)
        return True


    def remove_sales_coupon(self, item):
        if(not cfactory.delete_db_coupon(item.get_UID())):
            return False
        self.__all_coupons.remove(item)
        return True


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
        self.__all_items.append(item)
        item.save()
        return item

    def create_and_save_package(self, dict):
        #create and save package in database and current memory
        package = sfactory.create_package(dict)
        package.save()
        self.__all_packages.append(package)
        return package

    def create_and_save_service(self, dict):
        #create and save service in database and current memory
        service = sfactory.create_service(dict)
        service.save()
        self.__all_services.append(service)
        return service

    def get_all_receipt_by_name(self, username):
        users_receipt = []
        for i in self.__all_receipt:
            if i.user.get_username() == username:
                users_receipt.append(i)
        return users_receipt
    def create_and_save_coupon(self, dict):
        #create and save coupon in database and current memory
        coupon = cfactory.create_coupon(dict)
        self.__all_coupons.append(coupon)
        coupon.save()
        return coupon

    def get_all_receipt(self):
        return self.__all_receipt

    def get_all_appointments(self):
        return self.__all_appointment

    def get_all_appointment_by_username(self, username):
        list = []
        for i in self.__all_appointment:
            if(i.get_username() == username):
                list.append(i)
        return list
######################################################################
######################################################################
######################################################################
######################################################################
######################################################################
##############reduce stocks when buying items by users################
######################################################################
######################################################################
######################################################################
######################################################################



######################################
#for buying items
    def checkout_items_users(self, object_lists, ccoupon, users_details):
        print(ccoupon)
        sales_list = []
        subtotal_price = 0
        sales_rept = None
        for i in object_lists:
            #this is the getting of the item object, and calculating total price for each item * quantity.
            item_obj = self.get_item_by_UID(i['itemuid'])
            if(item_obj):
                quantity = i['quantity']
                stocks = item_obj.get_stocks()
                entry = sales_entry(item_obj, quantity)
                self.__all_items.remove(item_obj)
                sales_list.append(entry)
                subtotal_price = subtotal_price + entry.get_total_price()
                if(isinstance(item_obj, sales_items)):
                    item_obj.set_stocks(stocks - quantity)
                    item_obj.save()
                    self.__all_items.append(item_obj)
                print(ccoupon)
        if(ccoupon):
            total_amount = subtotal_price
            # using python function to create a unique id
            sales_rept = sales_receipt(str(uuid.uuid1()),sales_list, subtotal_price, ccoupon, users_details)
        else:
            sales_rept = sales_receipt(str(uuid.uuid1()),sales_list, subtotal_price,None, users_details)
        sales_rept.save()
        self.__all_receipt.append(sales_rept)
        return sales_rept


######################################
#for buying service
    def checkout_services_users(self, service, price,users_details):
        entry = sales_entry(service, 1)
        sales_rept = sales_receipt(str(uuid.uuid1()),[entry],price,  None, users_details)
        sales_rept.set_status_complete()
        sales_rept.save()
        self.__all_receipt.append(sales_rept)
        return sales_rept

#for keeping services appointment
    def create_appointment_and_save(self, date, time, user, servicename):
        doctor = self.get_doctor_for_services(servicename)
        appt = appointment(date, time, user, doctor, servicename)
        if(not appt):
            return False
        appt.save()
        self.__all_appointment.append(appt)
        return appt

    def complete_service_appointment(self, uid, status):
        for i in self.get_all_appointments():
            if(uid == i.get_UID()):
                i.set_status(status)
                i.save()
                return True
        return False

    def item_received_suppliers(self, itemuid, quantity):
        item = self.get_item_by_UID(itemuid)
        print(itemuid)
        if not item:
            print("item not found")
            return False
        self.__all_items.remove(item)
        stocks =item.get_stocks() + quantity
        item.set_stocks(stocks)
        item.save()
        self.__all_items.append(item)
        return True


    def get_doctors(self):
        doctorsDict = {}
        try:
            db = shelve.open(settings.DOCTOR_DB, 'r')
            doctorsDict = db['doctor']
            db.close()
        except:
            pass
        #
        doctorsList = []
        for key in doctorsDict:
            doctor = doctorsDict.get(key)
            doctorsList.append(doctor)
        return doctorsList

    def get_doctor_for_services(self, service_name):
        doctor = self.get_doctors()
        for i in doctor:
            if(i.get_Specialities() == service_name):
                return i
        rand = randint(0, len(doctor)-1)
        return doctor[rand]

    def get_doctor_by_uid(self, uid):
        doct = self.get_doctors()
        print(doct)
        for i in doct:
            if i.get_doctorID() == int(uid):
                return i
        return None



def get_all_appointments():
    s = shelve.open(settings.APPOINTMENT_DB)
    items = []
    try:
        for key in s:
            items.append(deserialize(s[key]))
    except Exception as e:
        print(e)
    finally:
        s.close()
    return items


def deserialize(dict):
    try:
        return pickle.loads(dict)
    except:
        return None

