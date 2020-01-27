from datetime import datetime
from backend.sales_entry import *
import pickle

class sales_receipt(object):
    def __init__(self,sales_UID, sales_entries, total,coupon, user ,  sales_datetime=datetime.today()):
        self.sales_UID = sales_UID
        self.sales_datetime = sales_datetime
        self.sales_entries = sales_entries #list of sales_items
        self.total = total
        self.coupon = coupon
        self.user = user


    def get_coupon(self):
        return self.coupon

    def set_coupon(self, coupon):
        self.coupon = coupon

    def get_UID(self):
        return self.sales_UID


    def set_sales_datetime(self, sales_datetime):
        self.sales_datetime = sales_datetime

    def get_sales_datetime(self):
        return self.sales_datetime

    def set_sales_entries(self, sales_entries):
        self.sales_entries = sales_entries

    def get_sales_entries(self):
        return self.sales_entries

    def set_coupon(self, coupon):
        self.coupon = coupon

    def get_discount(self):
        if(self.coupon):
            return self.coupon.get_discount(self.total)
        return 0

    def set_total(self, total):
        self.total = total

    def get_total(self):
        return self.total


    def save(self):
       s = shelve.open(settings.SALES_DB)
       try:
            s[self.sales_UID] = self.serialize()
            return True
       finally:
            s.close()
       return False

    def serialize(self):
        return pickle.dumps(self)
