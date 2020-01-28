class Feedback:
    countID = 0

    def __init__(self, firstName, email, category, feedback, status, date):
        Feedback.countID += 1
        self.__userID = Feedback.countID
        self.__firstName = firstName
        self.__category = category
        self.__feedback = feedback
        self.__status = status
        self.__email = email
        self.__date = date

    def get_userID(self):
        return self.__userID

    def get_firstName(self):
        return self.__firstName

    def get_category(self):
        return self.__category

    def get_feedback(self):
        return self.__feedback

    def get_status(self):
        return self.__status

    def get_email(self):
        return self.__email

    def get_date(self):
        return self.__date


    def set_userID(self, userID):
        self.__userID = userID

    def set_firstName(self,firstName):
        self.__firstName = firstName

    def set_category(self, category):
        self.__category = category

    def set_feedback(self, feedback):
        self.__feedback = feedback

    def set_status(self, status):
        self.__status = status

    def set_email(self, email):
        self.__email = email

    def set_date(self, date):
        self.__date = date
