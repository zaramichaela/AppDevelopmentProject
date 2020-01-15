
from backend.supplier import *
from backend.supplier_orders import *
from flask import flash
class suppliers_controller:
    def __init__(self):
        self.__all_suppliers = get_all_suppliers_db()
        self.__suppliers_orders = get_all_suppliers_orders()
        print(self.__all_suppliers)
        print(self.__suppliers_orders)

    def get_suppliers_by_UID(self, UID):
        #check and return 1 item finding via suppliers_UID. if more than 1, return None.
        for i in self.__all_suppliers:
            if(i.get_UID() == UID):
                return i
        return None

    def get_suppliers_orders_by_UID(self, oid):
        #check and return 1 item finding via suppliers_UID. if more than 1, return None.
        for i in self.__suppliers_orders:
            if(i.get_oid() == oid):
                return i
        return None


    def get_all_suppliers(self):
        print(self.__all_suppliers)
        return self.__all_suppliers

    def get_all_suppliers_orders(self):
        return self.__suppliers_orders

    def remove_sales_supplier_order(self, item):
        if(not delete_db_supplier_order(item.get_oid())):
            return False
        self.__suppliers_orders.remove(item)
        return True

    def update_sales_supplier(self, orderID, status):
        item = self.get_suppliers_orders_by_UID(orderID)
        item.set_progress()
        item.save()


    def create_and_save_suppliers(self, dict):

        supplier = create_suppliers(dict)
        print(supplier.get_UID())
        supplier.save()
        self.__all_suppliers.append(supplier)
        return supplier

    def create_and_save_supplier_order(self, dict):
        sup = self.get_suppliers_by_UID(dict['supplier'])
        if(not sup):
            flash("supplier not found, error", "error")

        supplier_order = create_supplier_orders(dict, sup)
        print(supplier_order)
        supplier_order.save()
        self.__suppliers_orders.append(supplier_order)
        return supplier_order

    def remove_supplier(self, item):
        ##TODO might need to remove any dependency or not? not sure.
        if(not delete_db_supplier(item.get_UID())):
            return False
        self.__all_suppliers.remove(item)
        return True


    def get_choice(self):
        all_choice = []
        for i in self.get_all_suppliers():
            temp = (i.get_UID(), i.get_UID())
            all_choice.append(temp)
        return all_choice

    def add_supplier(self, item):
        self.__all_suppliers.append(item)

    def add_supplier_order(self, item):
        self.__suppliers_orders.append(item)

def create_suppliers(dict):
    try:
        sup = suppliers(dict["UID"],dict["name"], dict["address"], dict["phone_num"], dict["product"], dict["price"])
        return sup
    except Exception as e:
        print(e)
        return None

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
        print(supplieruid)
        del s[supplieruid]
        return True
    except:
        return False
    finally:
        s.close()

def delete_db_supplier_order(supplieruid):
    #delete packages from shelve database
    s = shelve.open(settings.ORDER_DB)
    try:
        print(supplieruid)
        del s[supplieruid]
        return True
    except:
        return False
    finally:
        s.close()

def create_supplier_orders(dict, sup):
    try:
        order = supplier_orders( dict['UID'], sup.get_UID(), sup.get_name() , sup.get_product(), dict['number'], sup.get_price())
        return order
    except Exception as e:
        print(e)
        return None

def get_all_suppliers_orders():
    items = []
    s = shelve.open(settings.ORDER_DB)
    try:
        for key in s:
            items.append(deserialize(s[key]))
    finally:
        s.close()
    return items


def delete_db_supplier(UID):
    s = shelve.open(settings.SUPPLIERS_DB)
    try:
        del s[UID]
        return True
    finally:
        s.close()
    return False

def deserialize(dict):
    try:
        return pickle.loads(dict)
    except:
        return None

