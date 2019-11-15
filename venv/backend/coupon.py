import date as date
import backend.settings as settings
## coupon object
class Coupon:
    def __init__(self, UID, couponcode,percentage,discountlimit, minimumspent, expiredate):
        self.UID = UID
        self.couponcode = couponcode
        self.percentage = percentage
        self.discountlimit = discountlimit
        self.minimumspent = minimumspent
        self.expiredate = expiredate

    #check date expires
    def check_validity(self):
        if(date.today() > self.expiredate):
            return False
        return True

    #check validity
    #return discount amount
    #return discount limit if over the limit
    def get_discount(self, price):
        if(not self.check_validity):
            return 0
        try:
            discount = price/100 * self.percentage
            if(discount > self.discountlimit):
                return self.discountlimit
            return discount
        except:
            print("percentage cannot be 0")
            return 0



    def save(self):
       s = shelve.open(settings.COUPON_DB)
       try:
            s[self.UID] = self.serialize()
            return True
       finally:
            s.close()
       return False

    def save(self):
       s = shelve.open(settings.)
       try:
            s[self.UID] = self.serialize()
            return True
       finally:
            s.close()
       return False
