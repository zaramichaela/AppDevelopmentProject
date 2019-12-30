from backend.coupon import *
import shelve
import pickle

class coupon_factory:
    def __init__(self):
        pass

    def get_all_coupons(self):
        s = shelve.open(settings.COUPON_DB)
        error_flag = False
        try:
            self.all_coupons.append(self.unserialize_coupon(self.serialize_coupon(s[key])))
        except Exception as e:
            error_flag = True
        finally:
            s.close()
        return error_flag




    def unserialize_coupon(self, dict):
        try:
            return pickle.loads(dict)
        except:
            return None


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
