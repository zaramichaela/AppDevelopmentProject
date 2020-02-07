import datetime
import backend.settings as settings
import shelve
import pickle
import uuid



## appointment object
class appointment:
    def __init__(self, date, time, name):

        self.__UID = str(uuid.uuid1())
        self.__ordered_date = datetime.date.today()
        self.__date = date
        self.__time = time
        self.__name = name
        self.__status = "Confirmed"

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

    def get_ordered_date(self):
        return self.__ordered_date

    def get_name(self):
        return self.__name

    def get_UID(self):
        return self.__UID

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def set_date(self, date):
        self.__date = date

    def set_time(self, time):
        self.__time = time

    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)

  #run this to update the database
    def save(self):
        s = shelve.open(settings.APPOINTMENT_DB)
        try:
            s[self.__UID] = self.serialize()

            return True
        finally:
            s.close()
        return False

    def delete(self):
        s = shelve.open(settings.APPOINTMENT_DB)
        try:
            del s[self.__UID]
            return True
        finally:
            s.close()
        return False
