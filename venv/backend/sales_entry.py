from datetime import datetime
from backend import settings

#class represents each sales item made
#if needed can have subclass
class sales_entry:
    def __init__(self,sales_object, sales_datetime=datetime.now(), quantity=1):
        self.sales_datetime = sales_datetime
        self.sales_object = sales_object
        self.quantity = quantity

    def save(self):
       s = shelve.open(settings.SALES_DB)
       try:
            s[self.UID] = self.serialize()
            return True
       finally:
            s.close()
       return False

