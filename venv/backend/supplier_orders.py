from datetime import datetime
from backend import settings
import shelve
class supplier_orders:
    def __init__(self, oid, sid, sname, pname, amt = 1, unit_price,total_price, date_of_order=datetime.now()):
        self.__oid = oid
        self.__sid = sid
        self.__sname = sname
        self.__pname = pname
        self.__amt = amt
        self.__unit_price = unit_price
        self.__total_price = total_price
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
