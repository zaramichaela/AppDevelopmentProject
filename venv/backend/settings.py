from backend.itemscontroller import *
from login.login_controller import *
from backend.supplier_controller import *
#has the files location. allows easier editing

#database
ITEMS_DB = "databases/sales_item.db"
PACKAGES_DB = "databases/sales_packages.db"
SERVICES_DB = "databases/sales_service.db"
SALES_DB = "databases/sales.db"
COUPON_DB = "databases/coupon.db"
APPOINTMENT_DB = "databases/appointment.db"
DOCTOR_DB = "databases/doctor.db"
# ADMIN_DB = "admin.db"
# USER_DB = "user.db"
SUPPLIERS_DB = "databases/suppliers.db"
ORDER_DB = "databases/suppliers_order.db"
USER_ORDER_DB = "databases/user_order.db"
#images
ITEMSDIR= 'static/uploads/items/'
PACKAGEDIR = 'static/uploads/packages/'
SERVICEDIR = 'static/uploads/services/'
DOCTORDIR = 'static/uploads/doctors/'

itemcontroller = items_controller()
#logincontroller = login_controller()
suppliercontroller = suppliers_controller()
