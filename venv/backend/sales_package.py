import shelve
from backend import settings

#class for each package that contains multiple sessions and session remaining.
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

    #when users that has a package book a new session
    def book_session(self, datetime):
        self.remaining_sess -= 1

    def package_flag(self):
        return True

