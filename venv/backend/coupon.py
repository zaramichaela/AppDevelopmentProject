import datetime
import backend.settings as settings
import shelve
import pickle
## coupon object
class Coupon:
    def __init__(self, UID, couponcode,percentage,discountlimit, minimumspent, expiredate):
        self.__UID = UID
        self.__couponcode = couponcode
        self.set_percentage(percentage)
        self.set_discountlimit(discountlimit)
        self.set_minimumspent(minimumspent)
        self.set_expiry_date(expiredate)


    #set discount percentage
    #check if within percentage otherwise, set to 0
    def set_couponcode(self, couponcode):
        self.__couponcode = couponcode

    def set_minimumspent(self, minimumspent):
        self.__minimumspent = minimumspent

    #set expiry date, make sure it is in DD-MM-YYYY otherwise exception
    def set_expiry_date(self, expiredate):
        self.__expiredate = expiredate

    def set_percentage(self, percentage):
        self.__percentage = percentage

    #set discount limit amount.
    def set_discountlimit(self, discountlimit):
        self.__discountlimit = discountlimit


    #check date expires
    def check_validity(self):
        if(datetime.date.today() > self.expiredate):
            return False
        return True

    #check validity
    #return discount amount
    #return discount limit if over the limit
    def get_discount(self, price):
        if(not self.__check_validity):
            return 0
        try:
            discount = price/100 * self.percentage
            if(discount > self_discountlimit):
                return self.__discountlimit
            return discount
        except:
            print("percentage cannot be 0")
            return 0


    def serialize(self):
        return pickle.dumps(self)


    def get_UID(self):
        return self.__UID

    def get_couponcode(self):
        return self.__couponcode

    def get_percentage(self):
        return self.__percentage

    def get_minimumspent(self):
        return self.__minimumspent

    def get_discountlimit(self):
        return self.__discountlimit

    def get_expiredate(self):
        return self.__expiredate

    def save(self):
        s = shelve.open(settings.COUPON_DB)
        try:
            print(self.__UID)
            s[self.get_UID()] = self.serialize()
            return True
        finally:
            s.close()
        return False
