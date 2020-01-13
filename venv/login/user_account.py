
from werkzeug.security import generate_password_hash, check_password_hash
import shelve
import pickle


USER_DB = "user.db"

class user_account(object):

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)


    def get_username(self):
        return self.username

    def check_login(self, username, password):
        if(username == self.username and self.check_password(password)):
            return True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        s = shelve.open(USER_DB)
        try:
            s[self.username] = self.serialize()
            return True
        finally:
            s.close()
        return False

    #convert to pickle to store in shelve
    def serialize(self):
        return pickle.dumps(self)