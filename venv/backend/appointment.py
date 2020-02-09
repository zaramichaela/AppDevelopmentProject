import datetime
import backend.settings as settings
import shelve
import pickle
import uuid



## appointment object
class appointment:
    def __init__(self, date, time, user, doctor, servicename):
        self.UID = str(uuid.uuid1())
        self.ordered_date = datetime.datetime.now()
        self.date = date
        self.time = time
        self.user = user
        self.status = "Confirmed"
        self.doctor = doctor
        self.servicename = servicename

    def get_servicename(self):
        return self.servicename

    def get_username(self):
        return self.user.get_username()

    def set_servicename(self, servicename):
        self.servicename = servicename


    def get_address(self):
        return self.user.get_address()

    def get_doctor(self):
        return self.doctor

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_ordered_date(self):
        return self.ordered_date

    def get_name(self):
        return self.user.get_full_name()

    def get_UID(self):
        return self.UID

    def get_date(self):
        return self.date

    def set_date(self ,date):
        self.date = date

    def get_time(self):
        return self.time

    def set_date(self, date):
        self.date = date

    def set_time(self, time):
        self.time = time

    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)

  #run this to update the database
    def save(self):
        s = shelve.open(settings.APPOINTMENT_DB)
        try:
            s[self.UID] = self.serialize()

            return True
        finally:
            s.close()
        return False

    def delete(self):
        s = shelve.open(settings.APPOINTMENT_DB)
        try:
            del s[self.UID]
            return True
        finally:
            s.close()
        return False
