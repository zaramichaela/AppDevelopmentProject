from backend.coupon import *
import shelve
import pickle



class coupon_factory:
    def __init__(self):
        pass

    def get_all_coupons_db(self):
        s = shelve.open(settings.COUPON_DB)
        items = []
        try:
            for key in s:
                items.append(self.deserialize(s[key]))
        except Exception as e:
            print(e)
        finally:
            s.close()
        return items
####################################################################################
    def deserialize(self, dict):
        try:
            return pickle.loads(dict)
        except:
            return None
####################################################################################
    def create_coupon(self, dict):
        c1 = Coupon(dict['UID'], dict['couponcode'],dict['percentage'],dict['discountlimit'], dict['minimumspent'], dict['expiredate'])
        return c1
####################################################################################
    def check_coupon(self,coupon_code):
        #returns the coupons
        s = shelve.open(settings.COUPON_DB)
        all_coupons = []
        error_flag = False
        try:
            for key in s:
                all_coupons.append(self.create_coupon(s[key]))
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

####################################################################################    def delete_db_coupon(self, couponuid):
        #delete item from shelve database
        s = shelve.open(settings.COUPON_DB)
        try:
            del s[couponuid]
            return True
        except:
            return False
        finally:
            s.close()
