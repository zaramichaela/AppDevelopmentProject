from backend.sales_objects import sales_objects
from backend import settings


class sales_services(sales_objects):

    def __init__(self, UID,name, description, price, image_url):
        super().__init__(UID,name, description, price, image_url)

    #save function override
    #save in service database
    def save(self):
       s = shelve.open(settings.SERVICES_DB)
       try:
            s[self.UID] = self.serialize()
            return True
       finally:
            s.close()
       return False
