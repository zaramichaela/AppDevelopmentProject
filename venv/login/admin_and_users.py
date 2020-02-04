from werkzeug.security import generate_password_hash, check_password_hash

class Admin:
    countID = 0

    def __init__(self, username,  password):
        Admin.countID += 1
        self.__adminID = Admin.countID
        self.username = username
        self.set_password(password)

    def get_adminID(self):
        return self.__adminID

    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=10)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_adminID(self, adminID):
        self.__adminID = adminID

    def get_password(self):
        return self.password_hash


class User:
    countID = 0

    def __init__(self, username, email, password):
        User.countID += 1
        self.__userID = User.countID
        self.username = username
        self.email = email
        self.set_password(password)

    def get_userID(self):
        return self.__userID

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

#   def check_login(self, username, password):
#        if(username == self.username and self.check_password(password)):
#            return True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_userID(self, userID):
        self.__userID = userID

    def set_email(self, email):
        self.__email = email

    def get_password(self):
        return self.password_hash
