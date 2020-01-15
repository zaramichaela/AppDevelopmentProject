import shelve
from backend import settings
from datetime import date
from backend.sales_objects import *

#class for each package that contains multiple sessions and session remaining.
class sales_package(sales_objects):
    def __init__(self, UID,name, description, price, image_url, expiry_duration, sessions):
        super().__init__(UID,name, description, price, image_url)
        self._expiry_duration = expiry_duration #days to expiry date
        self._sessions = sessions
        self._remaining_sess = sessions
        self._bought_date = date.today()

    def check_expiry(self):
        if(self._bought_date+ timedelta(days=expiry_duration) <= datetime.today() ):
            return True
        else:
            return False

    def save(self):
       s = shelve.open(settings.PACKAGES_DB)
       try:
            s[self._UID] = self.serialize()
            return True
       finally:
            s.close()
       return False

    #when users that has a package book a new session
    def book_session(self, datetime):
        self._remaining_sess -= 1

    def package_flag(self):
        return True

    def get_sessions(self):
        return self._sessions

    def get_remaining_sessions(self):
        return self._remaining_sess

    def get_expiry_duration(self):
        return self._expiry_duration
