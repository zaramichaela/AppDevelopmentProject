class User:
    countID = 0

    def __init__(self, firstName, lastName, gender,):
        User.countID += 1
        self.__userID = User.countID
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender



    def get_userID(self):
        return self.__ID

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_gender(self):
        return self.__gender

    def set_userID(self, userID):
        self.__userID = userID

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

