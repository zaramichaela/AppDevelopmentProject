from datetime import datetime
from backend import settings
import shelve
import pickle
class supplier_orders:
    def __init__(self, oid, sid, sname, pname, amt, unit_price,progress="In-progress", date_of_order=datetime.now()):
        self.__oid = oid
        self.__sid = sid
        self.__sname = sname
        self.__pname = pname
        self.__amt = amt
        self.__unit_price = unit_price
        self.__total_price = amt * unit_price
        self.__progress = progress
        self.__date_of_order = date_of_order

    def get_oid(self):
        return self.__oid

    def set_oid (self,oid):
        self.__oid = oid

    def get_sid(self):
        return self.__sid

    def set_sid (self,sid):
        self.__sid = sid

    def get_sname(self):
        return self.__sname

    def set_sname(self,sname):
        self.__sname = sname

    def get_pname(self):
        return self.__pname

    def set_pname(self,pname):
        self.__pname = pname

    def get_amt(self):
        return self.__amt

    def set_amt(self,amt):
        self.__amt = amt

    def get_unit_price(self):
        return self.__unit_price

    def set_unit_price(self,unit_price):
        self.__unit_price = unit_price

    def get_total_price(self):
        return self.__total_price

    def set_total_price(self,total_price):
        self.__total_price = total_price

    def get_date_of_order(self):
        return self.__date_of_order

    def set_date_of_order(self,date_of_order):
        self.__date_of_order = date_of_order


    def get_progress(self):
        return self.__progress

    def set_progress(self,progress):
        self.__progress = progress


    def save(self):
       s = shelve.open(settings.ORDER_DB)
       try:
            s[self.__oid] = self.serialize()
            return True
       finally:
            s.close()
       return False


    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)
