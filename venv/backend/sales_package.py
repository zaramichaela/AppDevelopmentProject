import shelve
from backend import settings


class sales_package(sales_objects):
    def __init__(self, UID,name, description, price, image_url, expiry_duration, sessions,remaining_sess=sessions):
        super().__init__(UID,name, description, price, image_url)
        self.expiry_duration = expiry_duration
        self.sessions = sessions
        self.remaining_sess = remaining_sess

    def save(self):
       s = shelve.open(settings.PACKAGES_DB)
       try:
            s[self.UID] = self.serialize()
            return True
       finally:
            s.close()
       return False
