from datetime import datetime
from backend.sales_entry import *
import pickle

class sales_receipt(object):
    def __init__(self,sales_UID, sales_entries, total,coupon, user ,date_time=datetime.today(), status="Proccessing"):
        self.sales_UID = sales_UID
        self.sales_datetime = datetime.today()
        self.sales_entries = sales_entries #list of sales_items
        self.total = total
        self.coupon = coupon
        self.user = user
        self.status = status

    def get_date(self):
        return self.sales_datetime

    def get_number_entries(self):
        return len(self.sales_entries)

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

    def get_sub_total(self):
        return self.total

    def get_total(self):
        return self.total - self.get_discount()

    def save(self):
       s = shelve.open(settings.USER_ORDER_DB)
       try:
            s[self.sales_UID] = self.serialize()
            return True
       finally:
            s.close()
       return False

    def serialize(self):
        return pickle.dumps(self)

    def get_sales_count(self):
        return len(self.sales_entries)

    def get_status(self):
        return self.status

    def set_status_delivery(self):
        self.status = "In Transit"

    def set_status_complete(self):
        self.status = "Completed"

    def get_username(self):
        return self.user.get_username()

    def get_full_name(self):
        return self.user.get_full_name()

    def get_address(self):
        return self.user.get_address()
