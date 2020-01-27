

class user_details(object):
    def __init__(self,full_name ,country , street_addr, city, postal, phone, email, card_name, credit_card, exp_year, exp_month, CVV, user_login):
        self.full_name = full_name
        self.country = country
        self.street_addr = street_addr
        self.city = city
        self.postal = postal
        self.phone = phone
        self.email = email
        self.card_name = card_name
        self.credit_card = credit_card
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.CVV = CVV
        self.user_login = user_login


def create_user_details(dict, user_acc):
    user_det = user_details(dict['full_name'],dict['country'],dict['street_addr'],dict['city'],dict['postal'],dict['phone'],dict['email'],
                         dict['card_name'],dict['credit_card'],dict['exp_month'],dict['exp_year'], dict['CVV'], user_acc)
    return user_det
