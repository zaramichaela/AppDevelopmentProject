class customer_account:
    countID = 0

    def __init__(self, username, passwordhash):
        customer_account.countID += 1
        self.__customerID = customer_account.countID
        self.__username = username
        self.__passwordhash = passwordhash

    def get_customerID(self):
        return self.__customerID

    def get_username(self):
        return self.__username

    def get_passwordhash(self):
        return self.__passwordhash

    def set_customerID(self, customerID):
        self.__customerID = customerID

    def set_username(self, username):
        self.__username = username

    def set_passwordhash(self, passwordhash):
        self.__passwordhash = passwordhash
