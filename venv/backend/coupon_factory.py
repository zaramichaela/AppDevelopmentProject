from backend.coupon import *
import shelve

class coupon_factory:
    def __init__(self):
        pass

    #create coupon code with dictionary
    def create_coupon(self, dict):
        coupon(dict[''],)


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
