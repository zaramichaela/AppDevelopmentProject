
from backend.supplier import *

class suppliers_controller:
    def __init__(self):
        self.all_suppliers = get_all_suppliers_db()
        self.suppliers_orders = get_all_suppliers_orders()


    def get_suppliers_by_UID(self, UID):
        #check and return 1 item finding via suppliers_UID. if more than 1, return None.
        for i in self.all_suppliers:
            if(i.get_UID() == UID):
                return i
        return None

    def get_all_suppliers(self):
        print(self.all_suppliers)
        return self.all_suppliers

    def get_all_suppliers_orders(self):
        return self.suppliers_orders

    def remove_sales_supplier_order(self, item):
        if(not delete_db_supplier(item.get_UID())):
            return False
        self.all_suppliers.remove(item)
        return True

    def create_and_save_suppliers(self, dict):
        #create and save service in database and current memory
        supplier = create_suppliers(dict)
        print(supplier)
        supplier.save()
        self.all_suppliers.append(supplier)
        return supplier


    def remove_supplier(self, item):
        if(not delete_db_supplier(item.get_UID())):
            return False
        self.all_suppliers.remove(item)
        return True


def get_all_suppliers_db():
    items = []
    s = shelve.open(settings.SUPPLIERS_DB)
    try:
        for key in s:
            items.append(deserialize(s[key]))
    finally:
        s.close()
    return items

def delete_db_supplier(supplieruid):
    #delete packages from shelve database
    s = shelve.open(settings.SUPPLIERS_DB)
    try:
        del s[supplieruid]
        return True
    except:
        return False
    finally:
        s.close()


def get_all_suppliers_orders():
    items = []
    s = shelve.open(settings.ORDER_DB)
    try:
        for key in s:
            items.append(deserialize(s[key]))
    finally:
        s.close()
    return items

def create_suppliers(dict):
    try:
        sup = suppliers(dict["UID"],dict["name"], dict["address"], dict["phone_num"], dict["product"], dict["price"])
        return sup
    except Exception as e:
        print(e)
        return None

def delete_db_supplier(UID):
    items = []
    s = shelve.open(settings.SUPPLIERS_DB)
    try:
        for key in s:
            items.append(deserialize(s[key]))
    finally:
        s.close()
    return items

def deserialize(self, dict):
    try:
        return pickle.loads(dict)
    except:
        return None
