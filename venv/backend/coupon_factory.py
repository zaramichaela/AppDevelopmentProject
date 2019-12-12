from backend.coupon import *
import shelve

class coupon_factory:
    def __init__(self):
        self.all_coupons = []
        self.get_all_coupons()
        pass

    def get_all_coupons(self):
        s = shelve.open(settings.COUPON_DB)
        error_flag = False
        try:
            self.all_coupons.append(self.unserialize_coupon(self.serialize_coupon(s[key])))
        except:
            print(Exception)
            error_flag = True
        finally:
            s.close()
        return error_flag


    def get_coupon_by_UID(self, UID):
        coupon_item = [items for items in self.all_coupons if items.UID == UID]
        if(coupon_item == 1):
            return coupon_item[0]
        else:
            return None

    def get_coupon_by_code(self, couponcode):
        found_item = [items for items in self.all_coupons if items.couponcode == couponcode]
        if(len(found_item) == 1):
            return found_item
        else:
            return None

    def check_new_coupon(self, dict):
        if(not check_UID(dict['UID'])):
            return "Coupon UID is not unique, enter another UID"


    #create coupon code with dictionary
    def create_coupon(self, dict):
        if (self.check_new_coupon()):
            c1 = coupon(dict['UID'],dict['couponcode'],dict['percentage'],dict['discountlimit'],dict['minimumspent'],dict['expiredate'])

    def unserialize_coupon(self, dict):
        return coupon(dict['UID'],dict['couponcode'],dict['percentage'],dict['discountlimit'],dict['minimumspent'],dict['expiredate'])


    def delete_coupon(self, UID):
        s = shelve.open(settings.COUPON_DB)
        error_flag = False
        try:
            del s[UID]

        except:
            print(Exception)
            error_flag = True
        finally:
            s.close()
        return error_flag

    def check_coupon(self,coupon_code):
        #returns the coupons
        s = shelve.open(settings.COUPON_DB)
        all_coupons = []
        error_flag = False
        try:
            for key in s:
                all_coupons.append(create_coupon(s[key]))
        except:
            print(Exception)
            error_flag = True
        finally:
            s.close()
        if(error_flag):
            #ERROR return 0
            return None
        found_coupon = None
        for i in all_coupons:
            if(coupon_code == i.get_couponcode()):
                return i
        return None


        def from_json(cls, json_str):
            json_dict = json.loads(json_str)
            return cls(**json_dict)
