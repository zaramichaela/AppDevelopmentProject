import datetime as date
import backend.settings as settings
## coupon object
class Coupon:
    def __init__(self, UID, couponcode,percentage,discountlimit, minimumspent, expiredate):
        self.UID = UID
        self.couponcode = couponcode
        self.set_percentage(percentage)
        self.set_discountlimit(discountlimit)
        self.set_minimumspent(minimumspent)
        self.set_expiry_date(expiredate)

    #set discount percentage
    #check if within percentage otherwise, set to 0
    def set_couponcode(self, couponcode):
        self.couponcode = couponcode

    def set_minimumspent(self, minimumspent):
        self.minimumspent = minimumspent

    #set expiry date, make sure it is in DD-MM-YYYY otherwise exception
    def set_expiry_date(self, expiredate):
        try:
            datetime.datetime.strptime(date_text, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def set_percentage(self, percentage):
        if percentage >= 0 and percentage < 100:
            self.percentage = percentage
        else:
            self.percentage = 0

    #set discount limit amount.
    def set_discountlimit(self, discountlimit):
        self.discountlimit = discountlimit


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


    def serialize(self):
        if isinstance(self, date):
            serial = self.isoformat()
            return serial
        return self.__dict__

    def save(self):
       s = shelve.open(settings.COUPON_DB)
       try:
            s[self.UID] = self.serialize()
            return True
       finally:
            s.close()
       return False

    def get_UID(self):
        return self.UID
