class Doctor:
    countID = 0

    def __init__(self, Name, Specialities, gender, Profile, Status, Image):
        Doctor.countID += 1
        self.__doctorID = Doctor.countID
        self.__Name = Name
        self.__Specialities = Specialities
        self.__gender = gender
        self.__Profile = Profile
        self.__Status = Status
        self.__Image = Image

    def get_doctorID(self):
        return self.__doctorID

    def get_Name(self):
        return self.__Name

    def get_Specialities(self):
        return self.__Specialities

    def get_gender(self):
        return self.__gender

    def get_Profile(self):
        return self.__Profile

    def get_Status(self):
        return self.__Status

    def get_Image(self):
        return self.__Image


    def set_doctorID(self, doctorID):
        self.__doctorID = doctorID

    def set_Name(self, Name):
        self.__Name = Name

    def set_Specialities(self, Specialities):
        self.__Specialities = Specialities

    def set_gender(self, gender):
        self.__gender = gender

    def set_Profile(self, Profile):
        self.__Profile = Profile

    def set_Status(self, Status):
        self.__Status = Status

    def set_Image(self,Image):
        self.__Image = Image
