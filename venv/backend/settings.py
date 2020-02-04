from backend.itemscontroller import *
from login.login_controller import *
from backend.supplier_controller import *
#has the files location. allows easier editing
ITEMS_DB = "sales_item.db"
PACKAGES_DB = "sales_packages.db"
SERVICES_DB = "sales_service.db"
SALES_DB = "sales.db"
COUPON_DB = "coupon.db"
ADMIN_DB = "admin.db"
USER_DB = "user.db"
ITEMSDIR= 'static/uploads/items/'
PACKAGEDIR = 'static/uploads/packages/'
SERVICEDIR = 'static/uploads/services/'
DOCTORDIR = 'static/uploads/doctors/'
SUPPLIERS_DB = "suppliers.db"
ORDER_DB = "suppliers_order.db"
USER_ORDER_DB = "user_order.db"
itemcontroller = items_controller()
logincontroller = login_controller()
suppliercontroller = suppliers_controller()
