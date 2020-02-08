from flask import Blueprint, abort
from flask import render_template, request, flash,session,redirect, url_for
from backend.forms import *
from functools import wraps
# from login.forms import create_admin_account
from backend.settings import *
from login.user_account import *
from backend.doctorForm import CreatedoctorForm
from backend.Doctor import *
from login.forms import create_admin, AdminLogin,UserRegistration
from login.admin_and_users import *


admin_pages = Blueprint('admin_pages', __name__, template_folder='templates')

################### Authorization ##########################################
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if(session.get('admin_logged_in')):
            return f(*args, **kws)
        else:
            flash("You must log in as an admin first.")
            return redirect(url_for("admin_pages.admin"))
    return decorated_function
####################################################################################
# @admin_pages.route('/admin')
# def admin():
#     print(session.get('admin_logged_in'))
#     if not session.get('admin_logged_in'):
#         return render_template('admin/admin_login.html')
#     else:
#         return render_template('admin/admin_base.html')
# ####################################################################################
# @admin_pages.route('/admin/login', methods=['POST'])
# def do_admin_login():
#     username = request.form['username']
#     password = request.form['password']
#     if(logincontroller.login_admin(username, password)):
#         session['admin_logged_in'] = True
#         session['admin_username'] = request.form['username']
#     else:
#         flash('Wrong credentials!', "error")
#     return redirect(url_for("admin_pages.admin"))
####################################################################################
@admin_pages.route('/admin/logout')
@authorize
def admin_logout():
    session['admin_logged_in'] = False
    session['admin_username'] = ""
    return redirect(url_for("admin_pages.admin"))
####################################################################################
@admin_pages.route('/admin/add/coupons', methods= ['GET','POST'])
# admin needs to be logged in before he/she can view the contents of the page
# if not logged in, redirect to login page
@authorize
def add_coupons():
    # create an empty form from coupon form
    cform = coupon_form()
    if request.method == 'POST' and cform.validate():
        # if uid or coupon code already exists
        if(itemcontroller.get_coupon_by_UID(cform.UID.data) or itemcontroller.get_coupon_by_code(cform.couponcode.data)):
            flash("You have input an UID or coupon code that exists, please try again.", "error")
            return render_template('admin/adding/create_coupons.html', form=cform)
        # create a new coupon and save using itemcontroller (using cform data)
        new_coupon = itemcontroller.create_and_save_coupon(cform.data)
        # when new coupon is saved
        if(new_coupon.save()):
                flash("You have successfully create a new coupon for users to use.", "success")
    return render_template('admin/adding/create_coupons.html', form=cform)
####################################################################################
@admin_pages.route('/admin/add/services/', methods= ['GET','POST'])
@authorize
def add_shop_service():
    # create a new form for service
    form = new_service()

    if request.method == 'POST' and form.validate():
        # if service uid already exists
        if(itemcontroller.get_service_by_UID(form.UID.data)):
            flash("You have input an UID that exists, please try again.")
            return render_template('admin/adding/create_services.html', form=form)
        # get image data from form
        f = form.image.data
        # save uid form data into folder SERVICEDIR(in settings)/<uid name>
        f.save(SERVICEDIR + form.UID.data)
        # duplicate dictionary to change data
        update_form = form.data.copy()
        # add image url that was saved earlier into dictionary.
        # dictionary will be stored in sales_service.db
        update_form["image_url"] = SERVICEDIR + form.UID.data
        # save service using itemcontroller
        item = itemcontroller.create_and_save_service(update_form)
        # save again for the purpose of flash
        if (item.save()):
            flash("You have created a new service","success")
        else:
            flash("An error has occurred.","error")
    return render_template('admin/adding/create_services.html', form=form)
####################################################################################
@admin_pages.route('/admin/add/items/', methods= ['GET','POST'])
@authorize
def add_shop_item():
    # create new form for sales item
    form = new_sales_item()

    if request.method == 'POST' and form.validate():
        # check if uid for item exists
        if(itemcontroller.get_item_by_UID(form.UID.data)):
            flash("You have input an UID that exists, please try again.")
            return render_template('admin/adding/create_items.html', form=form)
        # get image data from form
        f = form.image.data
        # save uid form data into folder ITEMSDIR(in settings)/<uid name>
        f.save(ITEMSDIR + form.UID.data)
        # duplicate dictionary to change data
        update_form = form.data.copy()
        # add image url that was saved earlier into dictionary.
        # dictionary will be stored in sales_items.db
        update_form["image_url"] = ITEMSDIR + form.UID.data
        # save item using itemcontroller
        item = itemcontroller.create_and_save_item(update_form)
        # if item exists
        if (item):
            flash("You have created a new item","success")
        else:
            flash("A error has occurred.","error")
    return render_template('admin/adding/create_items.html', form=form)
####################################################################################
@admin_pages.route('/admin/add/packages/', methods= ['GET','POST'])
@authorize
def add_shop_package():
    # create new form for package
    form = new_package()

    if request.method == 'POST' and form.validate():
        # if uid for package already exists
        if(itemcontroller.get_package_by_UID(form.UID.data)):
            flash("You have input an UID that exists, please try again.")
            return render_template('admin/adding/create_packages.html', form=form)
        # get image data from form
        f = form.image.data
        # save uid form data into folder PACKAGEDIR(in settings)/<uid name>
        f.save(PACKAGEDIR + form.UID.data)
        # duplicate dictionary to change data
        update_form = form.data.copy()
        # add image url that was saved earlier into dictionary.
        # dictionary will be stored in sales_package.db
        update_form["image_url"] = PACKAGEDIR + form.UID.data
        # save package using itemcontroller
        item = itemcontroller.create_and_save_package(update_form)
        # if item exists
        if (item):
            flash("You have created a new package","success")
        # if item does not exist
        else:
            flash("A error has occurred.","error")
    return render_template('admin/adding/create_packages.html', form=form)
####################################################################################
@admin_pages.route('/admin/list/items')
@authorize
def list_sales_items():
    # get all sales items from itemcontroller
    sales = itemcontroller.get_all_sales_items()
    return render_template('admin/listing/list_sales_items.html', items=sales)
####################################################################################
@admin_pages.route('/admin/list/sales_packages')
@authorize
def list_sales_packages():
    # get all sales packages from itemcontroller
    sales = itemcontroller.get_all_sales_packages()
    return render_template('admin/listing/list_sales_packages.html', items=sales)
####################################################################################
@admin_pages.route('/admin/list/sales_services')
@authorize
def list_sales_services():
    # get all sales services from itemcontroller
    sales = itemcontroller.get_all_sales_services()
    return render_template('admin/listing/list_sales_services.html', items=sales)
####################################################################################
@admin_pages.route('/admin/list/coupons')
@authorize
def list_coupons():
    # get all coupons from itemcontroller
    sales = itemcontroller.get_all_coupons()
    return render_template('admin/listing/list_coupons.html', items=sales)
####################################################################################
####################################################################################
@admin_pages.route('/admin/list/appointments')
@authorize
def list_sales_appointments():
    # get all sales items from itemcontroller
    appt = itemcontroller.get_all_appointments()
    return render_template('admin/listing/list_appointments.html', items=appt)

#########################################################################################
@admin_pages.route('/admin/list/appointments/<uid>/complete')
@authorize
def complete_sales_appointments(uid):
    # get all sales items from itemcontroller
    flag = itemcontroller.complete_service_appointment(uid, "Completed")
    if flag:
        flash("Appointment has been completed.", "success")
    else:
        flash("Failed to find appointment, please refresh and try again", "error")
    return redirect(url_for("admin_pages.list_sales_appointments"))
#########################################################################################
############### deleting items and objects ########################################
#########################################################################################

@admin_pages.route('/admin/list/items/<itemid>/delete/', methods= ['GET','POST'])
@authorize
def delete_sales_item(itemid):
    # look for item using itemid in itemcontroller
    item = itemcontroller.get_item_by_UID(itemid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # else... remove the sales item
    flag = itemcontroller.remove_sales_item(item)
    # if flag exists
    if flag:
        flash("You have succeed in removing item " + item.get_UID(), "success")
    else:
        flash("There's been a error removing " + item.get_UID(), "error")
    return redirect(url_for("admin_pages.list_sales_items"))
####################################################################################
@admin_pages.route('/admin/list/items/<itemid>/invalidate/', methods= ['GET','POST'])
@authorize
def invalidate_sales_item(itemid):
    # look for item using itemid in itemcontroller
    item = itemcontroller.get_item_by_UID(itemid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # by default, flag is true
    flag = True
    # if flag is true, set to false
    # if flag is false, set to true
    if(item.get_available_flag()):
        flag = False
    else:
        flag = True
    # show the flag
    item.set_available_flag(flag)

    if flag:
        # if flag is True, it is available
        flash("You have set the item " + item.get_UID() + " to available", "success")
    else:
        # if flag is False, it is unavailable
        flash("You have set the item " + item.get_UID() + " to unavailable", "success")
    return redirect(url_for("admin_pages.list_sales_items"))
####################################################################################
@admin_pages.route('/admin/list/package/<packageid>/delete/', methods= ['GET','POST'])
@authorize
def delete_package(packageid):
    # look for item using packageid in itemcontroller
    item = itemcontroller.get_package_by_UID(packageid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # this flag is to see if there is an error in removing the package
    flag = itemcontroller.remove_sales_package(item)
    if flag:
        flash("You have succeed in removing item #" + item.get_UID(), "success")
    else:
        flash("There's been a error removing #" + item.get_UID(), "error")
    return redirect(url_for("admin_pages.list_sales_packages"))
####################################################################################
@admin_pages.route('/admin/list/packages/<packageid>/invalidate/', methods= ['GET','POST'])
@authorize
def invalidate_package(packageid):
    # look for item using packageid in itemcontroller
    item = itemcontroller.get_package_by_UID(packageid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # by default, flag is true
    flag = True
    # if flag is true, set to false
    # if flag is false, set to true
    if(item.get_available_flag()):
        flag = False
    else:
        flag = True
    # show the flag
    item.set_available_flag(flag)
    if flag:
        # if flag is True, it is available
        flash("You have set the package #" + item.get_UID() + " to available", "success")
    else:
        # if flag is False, it is unavailable
        flash("You have set the package #" + item.get_UID() + " to unavailable", "success")
    return redirect(url_for("admin_pages.list_sales_packages"))
####################################################################################
@admin_pages.route('/admin/list/service/<serviceid>/delete/', methods= ['GET','POST'])
@authorize
def delete_service(serviceid):
    # look for the serviceuid in itemcontroller
    item = itemcontroller.get_service_by_UID(serviceid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # this flag is to see if there is an error in removing the service
    flag = itemcontroller.remove_sales_service(item)
    if flag:
        flash("You have succeed in removing item " + item.get_UID(), "success")
    else:
        flash("There's been a error removing " + item.get_UID(), "error")
    return redirect(url_for("admin_pages.list_sales_services"))
####################################################################################
@admin_pages.route('/admin/list/service/<serviceid>/invalidate/', methods= ['GET','POST'])
@authorize
def invalidate_service(serviceid):
    # look for the serviceuid in itemcontroller
    item = itemcontroller.get_package_by_UID(serviceid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # by default, flag is true
    flag = True
    # if flag is true, set to false
    # if flag is false, set to true
    if(item.get_available_flag()):
        flag = False
    else:
        flag = True
    # show the flag
    item.set_available_flag(flag)
    if flag:
        flash("You have set the service #" + item.get_UID() + " to available", "success")
    else:
        flash("You have set the service #" + item.get_UID() + " to unavailable", "success")
    return redirect(url_for("admin_pages.list_sales_services"))
####################################################################################
@admin_pages.route('/admin/list/coupon/<couponid>/delete/', methods= ['GET','POST'])
@authorize
def delete_coupon(couponid):
    item = itemcontroller.get_coupon_by_UID(couponid)
    if(not item):
        abort(404)
    flag = itemcontroller.remove_sales_coupon(item)
    if flag:
        # if flag is True, it is available
        flash("You have succeed in removing item " + item.get_UID(),"success")
    else:
        # if flag is False, it is unavailable
        flash("There's been a error removing " + item.get_UID(), "error")
    return redirect(url_for("admin_pages.list_coupons"))
####################################################################################


#########################################################################################
############### editing each objects information ########################################
#########################################################################################

@admin_pages.route('/admin/list/items/<itemid>/edit/', methods= ['GET','POST'])
@authorize
def edit_item(itemid):
    # get item id from itemcontroller
    item = itemcontroller.get_item_by_UID(itemid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # create a new form to edit sales items
    form = edit_sales_item()
    if request.method == 'POST' and form.validate_on_submit():
        # get image from form
        file_ = request.files["image"]
        # save image into ITEMSDIR
        file_.save(ITEMSDIR+item.get_UID())
        # duplicate dictionary to change data
        update_form = form.data.copy()
        # add uid into dictionary that will be stored in sales_item.db
        update_form["UID"] = item.get_UID()
        # add image url that was saved earlier into dictionary.
        # dictionary will be stored in sales_item.db
        update_form["image_url"] = ITEMSDIR + item.get_UID()
        # remove old item from itemcontroller list and db
        itemcontroller.remove_sales_item(item)
        # create a new item and save it into db and itemcontroller
        item2 = itemcontroller.create_and_save_item(update_form)
        # if item2 (updated one) exists
        if (item2):
            flash("You have updated the item "+ item.get_UID() +" information", "success")
            return redirect(url_for("admin_pages.list_sales_items"))
        else:
        # if item2 (updated one) does not exist
            flash("A error has occurred.","error")
            # append item in itemcontroller
            itemcontroller.all_items.append(item)
            # save item
            item.save()
    else:
        # get the item name from form data
        form.name.data = item.get_name()
        # get the item category from form data
        form.category.data = item.get_category()
        # get the item discount from form data
        form.discount.data = item.get_discount()
        # get the item description from form data
        form.description.data = item.get_description()
        # get the item price from form data
        form.price.data = item.get_price()
        # get the item stocks from form data
        form.stocks.data = item.get_stocks()

    return render_template('admin/editing/edit_items.html', form=form, item=item)
####################################################################################

@admin_pages.route('/admin/list/packages/<packageid>/edit/', methods= ['GET','POST'])
@authorize
def edit_package(packageid):
    # get package uid from itemcontroller
    item = itemcontroller.get_package_by_UID(packageid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # create a new form to edit package form
    form = edit_package_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
        file_ = request.files["image"]
        if(file_):
            file_.save(PACKAGEDIR+item.get_UID())
        # duplicate dictionary to change data
        update_form = form.data.copy()
        # add uid into dictionary that will be stored in sales_item.db
        update_form["UID"] = item.get_UID()
        update_form["image_url"] = PACKAGEDIR +item.get_UID()
        itemcontroller.remove_sales_package(item)
        item2 = itemcontroller.create_and_save_package(update_form)
        if (item2):
            flash("You have updated the package "+ item2.get_UID() +" information", "success")
            return redirect(url_for("admin_pages.list_sales_packages"))
        else:
            flash("A error has occurred.","error")
            itemcontroller.all_packages(item)
            item.save()
    else:
            form.name.data = item.get_name()
            form.discount.data = item.get_discount()
            form.description.data = item.get_description()
            form.price.data = item.get_price()
            form.expiry_duration.data = item.get_expiry_duration()
            form.sessions.data = item.get_sessions()

    return render_template('admin/editing/edit_packages.html', form=form, item=item)
####################################################################################
@admin_pages.route('/admin/list/services/<serviceid>/edit/', methods= ['GET','POST'])
@authorize
def edit_service(serviceid):
    # get service uid from itemcontroller
    item = itemcontroller.get_service_by_UID(serviceid)
    # if item does not exist, 404
    if(not item):
        abort(404)
    # create a new form to edit service
    form = edit_service_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
        # get image from form
        file_ = request.files["image"]
        # if file exists
        if(file_):
        # save image into SERVICEDIR
            file_.save(SERVICEDIR+item.get_UID())
        # duplicate dictionary to change data
        update_form = form.data.copy()
        # add uid into dictionary that will be stored in sales_service.db
        update_form["UID"] = item.get_UID()
        # add image url that was saved earlier into dictionary.
        # dictionary will be stored in sales_item.db
        update_form["image_url"] = SERVICEDIR + item.get_UID()
        # remove old item from itemcontroller list and db
        itemcontroller.remove_sales_service(item)
        # create a new item and save it into db and itemcontroller
        item2 = itemcontroller.create_and_save_service(update_form)
        # if item2 exists
        if (item2):
            flash("You have updated the service "+ item2.get_UID() + "information", "success")
            return redirect(url_for("admin_pages.list_sales_services"))
        else:
            # if item2 (updated one) does not exist
            flash("A error has occurred.", "error")
            # append item in itemcontroller
            itemcontroller.all_services(item)
            # save
            item.save()
    else:
        # get the item name from form data
        form.name.data = item.get_name()
        # get the item discount from form data
        form.discount.data = item.get_discount()
        # get the item description from form data
        form.description.data = item.get_description()
        # get the item name from form data
        form.price.data = item.get_price()
    return render_template('admin/editing/edit_services.html', form=form, message=context, item=item)
####################################################################################
@admin_pages.route('/admin/list/coupons/<couponid>/edit/', methods= ['GET','POST'])
@authorize
def edit_coupon(couponid):
    item = itemcontroller.get_coupon_by_UID(couponid)
    if(not item):
        abort(404)
    form = edit_coupon_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():

        if(itemcontroller.get_coupon_by_code(form.couponcode.data)):
            flash("You have input an UID or coupon code that exists, please try again.", "error")
            return render_template('admin/editing/edit_coupons.html', form=form, item=item)
        itemcontroller.remove_sales_coupon(item)
        update_form = form.data.copy()
        update_form["UID"] = item.get_UID()
        print(item.get_UID())

        item2 = itemcontroller.create_and_save_coupon(update_form)
        if (item2):
            flash("You have updated the coupon "+ item.get_UID() +" information","success")
            return redirect(url_for("admin_pages.list_coupons"))
        else:
            flash("A error have occurred...", "error")
            itemcontroller.all_coupons(item)
            item.save()
    else:
            form.couponcode.data = item.get_couponcode()
            form.percentage.data = item.get_percentage()
            form.discountlimit.data = item.get_discountlimit()
            form.minimumspent.data = item.get_minimumspent()
            form.expiredate.data = item.get_expiredate()
    return render_template('admin/editing/edit_coupons.html', form=form, item=item)
####################################################################################
# @admin_pages.route('/admin/accounts/add', methods= ['GET','POST'])
# @authorize
# def create_admin_accounts():
#     context = {}
#     form = create_admin_account()
#     if request.method == 'POST' and form.validate():
#         success_flag = logincontroller.add_admin_account(form.username.data, form.password.data)
#         if (not success_flag):
#             flash("Error, you cannot create an account", "error")
#         else:
#             flash("Admin account created.", "success")
#         form = create_admin_account()
#     return render_template('admin/accounts/create_admin_accounts.html', form=form, message=context)
####################################################################################
# @admin_pages.route('/admin/accounts/admin/view')
# @authorize
# def list_admin_accounts():
#     context = {}
#     items = logincontroller.get_all_admins()
#     return render_template('admin/accounts/list_admin_accounts.html',items=items)
# ####################################################################################
# @admin_pages.route('/admin/accounts/admins/<username>/delete/')
# @authorize
# def del_admin_account(username):
#     flag = logincontroller.find_admin_username(username)
#     if flag:
#         a = logincontroller.delete_admin_account(username)
#         flash("You have deleted the admin user " + username, "success")
#     else:
#         flash("An error has occurred, please try again", "error")
#         abort(404)
#     return redirect(url_for("admin_pages.list_admin_accounts"))
# ####################################################################################
# @admin_pages.route('/admin/accounts/admin/changepassword/', methods= ['GET','POST'])
# @authorize
# def change_admin_password():
#     context={}
#     item = logincontroller.find_user_username(session['admin_username'])
#     form = edit_admin_account()
#     if(request.method == "POST" and form.validate()):
#         username = session["admin_username"]
#         logincontroller.change_admin_password(username, form.old_password.data, form.password.data)
#     return render_template('admin/accounts/edit_admin_accounts.html',form =form,message=context)
# ####################################################################################
# @admin_pages.route('/admin/accounts/users/view')
# @authorize
# def list_users_accounts():
#     context = {}
#     items = logincontroller.get_all_users()
#     return render_template('admin/accounts/list_users_accounts.html',items=items)
####################################################################################
@admin_pages.route('/admin/accounts/users/<username>/delete/')
@authorize
def del_user_account(username):
    item = logincontroller.find_user_username(username)
    if(not item):
        abort(404)
    if item:
        flash("You have deleted the user " + username, "success")
        logincontroller.del_user_account(username)
    else:
        flash("an error have occurred, please try again", "error")
    items = logincontroller.get_all_admins()
    return redirect(url_for("admin_pages.list_users_accounts"))
####################################################################################
@admin_pages.route('/admin/accounts/users/<username>/ban/')
@authorize
def ban_user_account(username):
    user = logincontroller.find_user_username(username)
    if(not user):
        abort(404)
    if user:
        flash("You have ban the user " + username, "success")
        if(user.get_ban_flag()):
            logincontroller.set_ban_user_flag(user, False)
        else:
            logincontroller.set_ban_user_flag(user, True)
    else:
        flash("An error has occurred, please try again", "error")
    items = logincontroller.get_all_admins()
    return redirect(url_for("admin_pages.list_users_accounts"))
####################################################################################



###########################################################################
##########################################################################
###########################################################################
##########################################################################
###########################################################################
##########################################################################
#for suppliers#############################################################
##########################################################################
@admin_pages.route('/admin/suppliers/add', methods= ['GET','POST'])
@authorize
def create_suppliers():
    form = create_supplier()
    if request.method == 'POST' and form.validate():
        if(suppliercontroller.get_suppliers_by_UID(form.UID.data)):
            flash("Error, UID exists, please choose another UID", "error")
            return render_template('admin/suppliers/create_suppliers.html', form=form)
        success_flag = suppliercontroller.create_and_save_suppliers(form.data)
        if (not success_flag):
            flash("Error, you cannot list a new supplier", "error")
        else:
            flash("A new supplier has been listed", "success")
    return render_template('admin/suppliers/create_suppliers.html', form=form)
####################################################################################
@admin_pages.route('/admin/suppliers/<supplierid>/edit', methods= ['GET','POST'])
@authorize
def edit_suppliers(supplierid):
    item = suppliercontroller.get_suppliers_by_UID(supplierid)
    if(not item):
        abort(404)
    form = create_supplier(formdata=request.form)

    if request.method == 'POST' and form.validate():
        suppliercontroller.remove_supplier(item)
        new_item = suppliercontroller.create_and_save_suppliers(form.data)
        if (not new_item):
            flash("Error, you cannot edit the supplier " + item.get_UID(), "error")
            return redirect(url_for("admin_pages.list_suppliers"))
        else:
            flash("You have edited the supplier", "success")
            return redirect(url_for("admin_pages.list_suppliers"))
    else:
            form.UID.data = item.get_UID()
            form.name.data = item.get_name()
            form.p_UID.data = item.get_pUID()
            form.address.data = item.get_address()
            form.phone_num.data = item.get_phone_num()
            form.product.data = item.get_product()
            form.price.data = item.get_price()
    return render_template('admin/suppliers/edit_suppliers.html', form=form)
####################################################################################
@admin_pages.route('/admin/suppliers/<supplierid>/delete', methods= ['GET','POST'])
@authorize
def delete_suppliers(supplierid):
    supplier = suppliercontroller.get_suppliers_by_UID(supplierid)
    if(not supplier):
        abort(404)
    success_flag = suppliercontroller.remove_supplier(supplier)
    if (not success_flag):
        flash("Error, you cannot delete the supplier " + supplier.get_UID() , "error")
    else:
        flash("The supplier" + supplier.get_UID() +  " has been deleted", "success")
    return redirect(url_for("admin_pages.list_suppliers"))
####################################################################################
@admin_pages.route('/admin/suppliers/view')
@authorize
def list_suppliers():
    context = {}
    items = suppliercontroller.get_all_suppliers()
    return render_template('admin/suppliers/list_suppliers.html',items=items)
####################################################################################
@admin_pages.route('/admin/suppliersorders/view')
@authorize
def list_suppliers_orders():
    context = {}
    items = suppliercontroller.get_all_suppliers_orders()
    return render_template('admin/suppliers/list_suppliers_orders.html',items=items)
####################################################################################
@admin_pages.route('/admin/suppliersorders/add', methods= ['GET','POST'])
@authorize
def create_suppliers_orders():
    form = buy_orders_supplier()
    form.supplier.choices = suppliercontroller.get_choice()
    if request.method == 'POST' and form.validate():

        if(suppliercontroller.get_suppliers_orders_by_UID(form.UID.data)):
            flash("Error, UID exists, please choose another UID", "error")
        #   print("GG")
            return render_template('admin/suppliers/create_suppliers_orders.html', form=form)
        success_flag = suppliercontroller.create_and_save_supplier_order(form.data)
        if (not success_flag):
            flash("Error, you cannot make a new order", "error")
        else:
            flash("A new order has been made", "success")
            return redirect(url_for("admin_pages.list_suppliers_orders"))
    return render_template('admin/suppliers/create_suppliers_orders.html', form=form)
####################################################################################
@admin_pages.route('/admin/suppliersorders/<orderid>/cancel', methods= ['GET','POST'])
@authorize
def cancel_suppliers_order(orderid):
    item = suppliercontroller.get_suppliers_orders_by_UID(orderid)
    if(not item):
        abort(404)
    suppliercontroller.update_sales_supplier(orderid, "Cancelled")
    flash("you have cancelled the order.", "success")
    return redirect(url_for("admin_pages.list_suppliers_orders"))
####################################################################################
@admin_pages.route('/admin/suppliersorders/<orderid>/received', methods= ['GET','POST'])
@authorize
def received_suppliers_order(orderid):
    item = suppliercontroller.get_suppliers_orders_by_UID(orderid)
    if(not item):
        abort(404)
    suppliercontroller.update_sales_supplier(orderid, "Received")
    flag = itemcontroller.item_received_suppliers(item.get_pUID(), item.get_amt())
    if(flag):
        flash("you have received the order, item quantity has been added to the store.", "success")
    else:
        flash("you have received the order, but item does not exists, please add item manually.", "success")
    return redirect(url_for("admin_pages.list_suppliers_orders"))
####################################################################################
@admin_pages.route('/admin/retrieveFeedback')
@authorize
def retrieveFeedback():
    usersDict = {}
    db = shelve.open('feedstorage.db', 'r')
    usersDict = db['Feedback']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)

    return render_template('/admin/feedback/retrieveFeedback.html', usersList = usersList, count = len(usersList))
####################################################################################
@admin_pages.route('/admin/deleteFeedback/<int:id>', methods=['POST'])
@authorize
def deleteFeedback(id):
    usersDict = {}
    db = shelve.open('feedstorage.db', 'w')
    usersDict = db['Feedback']
    usersDict.pop(id)
    db['Feedback'] = usersDict
    db.close()

    return redirect(url_for('admin_pages.retrieveFeedback'))
####################################################################################
@admin_pages.route('/admin/updateFeedback/<int:id>/', methods = ['GET', 'POST'])
@authorize
def updateFeedback(id):
    updateFeedbackForm = UpdateFeedbackForm(request.form)

    if request.method == 'POST' and updateFeedbackForm.validate():
        userDict = {}
        print("GG")
        db = shelve.open('feedstorage.db', 'w')
        userDict = db['Feedback']

        feedback = userDict.get(id)
        feedback.set_status(updateFeedbackForm.status.data)

        db['Feedback'] = userDict
        db.close()

        return redirect(url_for('admin_pages.retrieveFeedback'))
    else:
        userDict = {}
        db = shelve.open('feedstorage.db', 'w')
        userDict = db['Feedback']
        db.close()

        feedback = userDict.get(id)
        updateFeedbackForm.firstName.data = feedback.get_firstName()
        updateFeedbackForm.email.data = feedback.get_email()
        updateFeedbackForm.category.data = feedback.get_category()
        updateFeedbackForm.feedback.data = feedback.get_feedback()
        updateFeedbackForm.status.data = feedback.get_status()

        return render_template('/admin/feedback/updateFeedback.html', form = updateFeedbackForm)
labels = []
values = []
colors = [
    "#E27D60", "#85DCB", "#E8A87C", "#C38D9E",
    "#41B3A3", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
####################################################################################
@admin_pages.route('/admin/feedback/stats')
def stats():
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()
    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')

    TotalList = []
    JanList = []
    FebList = []
    MarList = []
    AprList = []
    MayList = []
    JunList = []
    JulList = []
    AugList = []
    SepList = []
    OctList = []
    NovList = []
    DecList = []
    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        TotalList.append(count)

        if datesplit[1] == '01':
            JanList.append(count)
        elif datesplit[1] == '02':
            FebList.append(count)
        elif datesplit[1] == '03':
            MarList.append(count)
        elif datesplit[1] == '04':
            AprList.append(count)
        elif datesplit[1] == '05':
            MayList.append(count)
        elif datesplit[1] == '06':
            JunList.append(count)
        elif datesplit[1] == '07':
            JulList.append(count)
        elif datesplit[1] == '08':
            AugList.append(count)
        elif datesplit[1] == '09':
            SepList.append(count)
        elif datesplit[1] == '10':
            OctList.append(count)
        elif datesplit[1] == '11':
            NovList.append(count)
        elif datesplit[1]:
            DecList.append(count)

    return render_template('admin/feedback/Stats.html', TotalList = TotalList, JanList = JanList, FebList = FebList, MarList = MarList, AprList = AprList, MayList = MayList, JunList = JunList, JulList = JulList, AugList = AugList, SepList = SepList, OctList = OctList, NovList = NovList, DecList = DecList,
                           count = len(TotalList), jancount = len(JanList), febcount = len(FebList), marcount = len(MarList), aprcount = len(AprList), maycount = len(MayList), juncount = len(JunList), julcount = len(JulList), augcount = len(AugList), sepcount = len(SepList), octcount = len(OctList), novcount = len(NovList), deccount = len(DecList))
####################################################################################
@admin_pages.route('/admin/feedback/statgraph')
def stats1():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

#overall
    TotalList = []
    JanList = []
    FebList = []
    MarList = []
    AprList = []
    MayList = []
    JunList = []
    JulList = []
    AugList = []
    SepList = []
    OctList = []
    NovList = []
    DecList = []

#general
    JanGenList = []
    FebGenList = []
    MarGenList = []
    AprGenList = []
    MayGenList = []
    JunGenList = []
    JulGenList = []
    AugGenList = []
    SepGenList = []
    OctGenList = []
    NovGenList = []
    DecGenList = []

#Products
    JanProdList = []
    FebProdList = []
    MarProdList = []
    AprProdList = []
    MayProdList = []
    JunProdList = []
    JulProdList = []
    AugProdList = []
    SepProdList = []
    OctProdList = []
    NovProdList = []
    DecProdList = []

#Treatment
    JanTreatList = []
    FebTreatList = []
    MarTreatList = []
    AprTreatList = []
    MayTreatList = []
    JunTreatList = []
    JulTreatList = []
    AugTreatList = []
    SepTreatList = []
    OctTreatList = []
    NovTreatList = []
    DecTreatList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        TotalList.append(count)
        cat = str(count.get_category())

        if datesplit[1] == '01':
            JanList.append(count)
        elif datesplit[1] == '02':
            FebList.append(count)
        elif datesplit[1] == '03':
            MarList.append(count)
        elif datesplit[1] == '04':
            AprList.append(count)
        elif datesplit[1] == '05':
            MayList.append(count)
        elif datesplit[1] == '06':
            JunList.append(count)
        elif datesplit[1] == '07':
            JulList.append(count)
        elif datesplit[1] == '08':
            AugList.append(count)
        elif datesplit[1] == '09':
            SepList.append(count)
        elif datesplit[1] == '10':
            OctList.append(count)
        elif datesplit[1] == '11':
            NovList.append(count)
        elif datesplit[1]:
            DecList.append(count)

        #generalList
        if datesplit[1] == '01' and cat == 'G':
            JanGenList.append(count)
        elif datesplit[1] == '02' and cat == 'G':
            FebGenList.append(count)
        elif datesplit[1] == '03' and cat == 'G':
            MarGenList.append(count)
        elif datesplit[1] == '04' and cat == 'G':
            AprGenList.append(count)
        elif datesplit[1] == '05' and cat == 'G':
            MayGenList.append(count)
        elif datesplit[1] == '06' and cat == 'G':
            JunGenList.append(count)
        elif datesplit[1] == '07' and cat == 'G':
            JulGenList.append(count)
        elif datesplit[1] == '08' and cat == 'G':
            AugGenList.append(count)
        elif datesplit[1] == '09' and cat == 'G':
            SepGenList.append(count)
        elif datesplit[1] == '10' and cat == 'G':
            OctGenList.append(count)
        elif datesplit[1] == '11' and cat == 'G':
            NovGenList.append(count)
        elif datesplit[1] == '12' and cat == 'G':
            DecGenList.append(count)


        #ProductList
        if datesplit[1] == '01' and cat == 'P':
            JanProdList.append(count)
        elif datesplit[1] == '02' and cat == 'P':
            FebProdList.append(count)
        elif datesplit[1] == '03' and cat == 'P':
            MarProdList.append(count)
        elif datesplit[1] == '04' and cat == 'P':
            AprProdList.append(count)
        elif datesplit[1] == '05' and cat == 'P':
            MayProdList.append(count)
        elif datesplit[1] == '06' and cat == 'P':
            JunProdList.append(count)
        elif datesplit[1] == '07' and cat == 'P':
            JulProdList.append(count)
        elif datesplit[1] == '08' and cat == 'P':
            AugProdList.append(count)
        elif datesplit[1] == '09' and cat == 'P':
            SepProdList.append(count)
        elif datesplit[1] == '10' and cat == 'P':
            OctProdList.append(count)
        elif datesplit[1] == '11' and cat == 'P':
            NovProdList.append(count)
        elif datesplit[1] == '12' and cat == 'P':
            DecProdList.append(count)


        #TreatmentList
        if datesplit[1] == '01' and cat == 'T':
            JanTreatList.append(count)
        elif datesplit[1] == '02' and cat == 'T':
            FebTreatList.append(count)
        elif datesplit[1] == '03' and cat == 'T':
            MarTreatList.append(count)
        elif datesplit[1] == '04' and cat == 'T':
            AprTreatList.append(count)
        elif datesplit[1] == '05' and cat == 'T':
            MayTreatList.append(count)
        elif datesplit[1] == '06' and cat == 'T':
            JunTreatList.append(count)
        elif datesplit[1] == '07' and cat == 'T':
            JulTreatList.append(count)
        elif datesplit[1] == '08' and cat == 'T':
            AugTreatList.append(count)
        elif datesplit[1] == '09' and cat == 'T':
            SepTreatList.append(count)
        elif datesplit[1] == '10' and cat == 'T':
            OctTreatList.append(count)
        elif datesplit[1] == '11' and cat == 'T':
            NovTreatList.append(count)
        elif datesplit[1] == '12' and cat == 'T':
            DecTreatList.append(count)

    return render_template('admin/feedback/StatGraph.html', title = 'Feedback - Statistics(Graph)', max = 20, labels = bar_labels, values = bar_values, TotalList = TotalList, JanList = JanList, FebList = FebList, MarList = MarList, AprList = AprList, MayList = MayList, JunList = JunList, JulList = JulList, AugList = AugList, SepList = SepList, OctList = OctList, NovList = NovList, DecList = DecList,
                           count = len(TotalList), jancount = len(JanList), febcount = len(FebList), marcount = len(MarList), aprcount = len(AprList), maycount = len(MayList), juncount = len(JunList), julcount = len(JulList), augcount = len(AugList), sepcount = len(SepList), octcount = len(OctList), novcount = len(NovList), deccount = len(DecList),
                           JanGenList = JanGenList, FebGenList = FebGenList, MarGenList = MarGenList, AprGenList = AprGenList, MayGenList = MayGenList, JunGenList = JunGenList, JulGenList = JulGenList, AugGenList = AugGenList, SepGenList = SepGenList, OctGenList = OctGenList, NovGenList = NovGenList, DecGenList = DecGenList,
                            jangencount = len(JanGenList), febgencount = len(FebGenList), margencount = len(MarGenList), aprgencount = len(AprGenList), maygencount = len(MayGenList), jungencount = len(JunGenList), julgencount = len(JulGenList), auggencount = len(AugGenList), sepgencount = len(SepGenList), octgencount = len(OctGenList), novgencount = len(NovGenList), decgencount = len(DecGenList),
                           JanProdList = JanProdList, FebProdList = FebProdList, MarProdList = MarProdList, AprProdList = AprProdList, MayProdList = MayProdList, JunProdList = JunProdList, JulProdList = JulProdList, AugProdList = AugProdList, SepProdList = SepProdList, OctProdList = OctProdList, NovProdList = NovProdList, DecProdList = DecProdList,
                            janprodcount = len(JanProdList), febprodcount = len(FebProdList), marprodcount = len(MarProdList), aprprodcount = len(AprProdList), mayprodcount = len(MayProdList), junprodcount = len(JunProdList), julprodcount = len(JulProdList), augprodcount = len(AugProdList), sepprodcount = len(SepProdList), octprodcount = len(OctProdList), novprodcount = len(NovProdList), decprodcount = len(DecProdList),
                           JanTreatList = JanTreatList, FebTreatList = FebTreatList, MarTreatList = MarTreatList, AprTreatList = AprTreatList, MayTreatList = MayTreatList, JunTreatList = JunTreatList, JulTreatList = JulTreatList, AugTreatList = AugTreatList, SepTreatList = SepTreatList, OctTreatList = OctTreatList, NovTreatList = NovTreatList, DecTreatList = DecTreatList,
                            jantreatcount = len(JanTreatList), febtreatcount = len(FebTreatList), martreatcount = len(MarTreatList), aprtreatcount = len(AprTreatList), maytreatcount = len(MayTreatList), juntreatcount = len(JunTreatList), jultreatcount = len(JulTreatList), augtreatcount = len(AugTreatList), septreatcount = len(SepTreatList), octtreatcount = len(OctTreatList), novtreatcount = len(NovTreatList), dectreatcount = len(DecTreatList))
####################################################################################

#Stat-Gen
@admin_pages.route('/admin/feedback/StatGen')
@authorize
def CatGen():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

    JanGenList = []
    FebGenList = []
    MarGenList = []
    AprGenList = []
    MayGenList = []
    JunGenList = []
    JulGenList = []
    AugGenList = []
    SepGenList = []
    OctGenList = []
    NovGenList = []
    DecGenList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        cat = str(count.get_category())

        if datesplit[1] == '01' and cat == 'G':
            JanGenList.append(count)
        elif datesplit[1] == '02' and cat == 'G':
            FebGenList.append(count)
        elif datesplit[1] == '03' and cat == 'G':
            MarGenList.append(count)
        elif datesplit[1] == '04' and cat == 'G':
            AprGenList.append(count)
        elif datesplit[1] == '05' and cat == 'G':
            MayGenList.append(count)
        elif datesplit[1] == '06' and cat == 'G':
            JunGenList.append(count)
        elif datesplit[1] == '07' and cat == 'G':
            JulGenList.append(count)
        elif datesplit[1] == '08' and cat == 'G':
            AugGenList.append(count)
        elif datesplit[1] == '09' and cat == 'G':
            SepGenList.append(count)
        elif datesplit[1] == '10' and cat == 'G':
            OctGenList.append(count)
        elif datesplit[1] == '11' and cat == 'G':
            NovGenList.append(count)
        elif datesplit[1] == '12' and cat == 'G':
            DecGenList.append(count)
    return render_template('admin/feedback/StatGen.html', title = 'Feedback - Category(General)', max = 20, labels = bar_labels, values = bar_values, JanGenList = JanGenList, FebGenList = FebGenList, MarGenList = MarGenList, AprGenList = AprGenList, MayGenList = MayGenList, JunGenList = JunGenList, JulGenList = JulGenList, AugGenList = AugGenList, SepGenList = SepGenList, OctGenList = OctGenList, NovGenList = NovGenList, DecGenList = DecGenList,
                    jangencount = len(JanGenList), febgencount = len(FebGenList), margencount = len(MarGenList), aprgencount = len(AprGenList), maygencount = len(MayGenList), jungencount = len(JunGenList), julgencount = len(JulGenList), auggencount = len(AugGenList), sepgencount = len(SepGenList), octgencount = len(OctGenList), novgencount = len(NovGenList), decgencount = len(DecGenList))


#Stat-Prod
@admin_pages.route('/admin/feedback/StatProd')
@authorize
def CatProd():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

    JanProdList = []
    FebProdList = []
    MarProdList = []
    AprProdList = []
    MayProdList = []
    JunProdList = []
    JulProdList = []
    AugProdList = []
    SepProdList = []
    OctProdList = []
    NovProdList = []
    DecProdList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        cat = str(count.get_category())

        if datesplit[1] == '01' and cat == 'P':
            JanProdList.append(count)
        elif datesplit[1] == '02' and cat == 'P':
            FebProdList.append(count)
        elif datesplit[1] == '03' and cat == 'P':
            MarProdList.append(count)
        elif datesplit[1] == '04' and cat == 'P':
            AprProdList.append(count)
        elif datesplit[1] == '05' and cat == 'P':
            MayProdList.append(count)
        elif datesplit[1] == '06' and cat == 'P':
            JunProdList.append(count)
        elif datesplit[1] == '07' and cat == 'P':
            JulProdList.append(count)
        elif datesplit[1] == '08' and cat == 'P':
            AugProdList.append(count)
        elif datesplit[1] == '09' and cat == 'P':
            SepProdList.append(count)
        elif datesplit[1] == '10' and cat == 'P':
            OctProdList.append(count)
        elif datesplit[1] == '11' and cat == 'P':
            NovProdList.append(count)
        elif datesplit[1] == '12' and cat == 'P':
            DecProdList.append(count)
    return render_template('admin/feedback/StatProd.html', title = 'Feedback - Category(Products)', max = 20, labels = bar_labels, values = bar_values, JanProdList = JanProdList, FebProdList = FebProdList, MarProdList = MarProdList, AprProdList = AprProdList, MayProdList = MayProdList, JunProdList = JunProdList, JulProdList = JulProdList, AugProdList = AugProdList, SepProdList = SepProdList, OctProdList = OctProdList, NovProdList = NovProdList, DecProdList = DecProdList,
                    janprodcount = len(JanProdList), febprodcount = len(FebProdList), marprodcount = len(MarProdList), aprprodcount = len(AprProdList), mayprodcount = len(MayProdList), junprodcount = len(JunProdList), julprodcount = len(JulProdList), augprodcount = len(AugProdList), sepprodcount = len(SepProdList), octprodcount = len(OctProdList), novprodcount = len(NovProdList), decprodcount = len(DecProdList))



#Stat-Treat
@admin_pages.route('/admin/feedback/StatTreat')
@authorize
def CatTreat():
    bar_labels = labels
    bar_values = values
    db = shelve.open('feedstorage.db', 'r')
    countDict = db['Feedback']
    db.close()

    JanTreatList = []
    FebTreatList = []
    MarTreatList = []
    AprTreatList = []
    MayTreatList = []
    JunTreatList = []
    JulTreatList = []
    AugTreatList = []
    SepTreatList = []
    OctTreatList = []
    NovTreatList = []
    DecTreatList = []

    for key in countDict:
        count = countDict.get(key)
        date = str(count.get_date())
        datesplit = date.split('-')
        cat = str(count.get_category())

        if datesplit[1] == '01' and cat == 'T':
            JanTreatList.append(count)
        elif datesplit[1] == '02' and cat == 'T':
            FebTreatList.append(count)
        elif datesplit[1] == '03' and cat == 'T':
            MarTreatList.append(count)
        elif datesplit[1] == '04' and cat == 'T':
            AprTreatList.append(count)
        elif datesplit[1] == '05' and cat == 'T':
            MayTreatList.append(count)
        elif datesplit[1] == '06' and cat == 'T':
            JunTreatList.append(count)
        elif datesplit[1] == '07' and cat == 'T':
            JulTreatList.append(count)
        elif datesplit[1] == '08' and cat == 'T':
            AugTreatList.append(count)
        elif datesplit[1] == '09' and cat == 'T':
            SepTreatList.append(count)
        elif datesplit[1] == '10' and cat == 'T':
            OctTreatList.append(count)
        elif datesplit[1] == '11' and cat == 'T':
            NovTreatList.append(count)
        elif datesplit[1] == '12' and cat == 'T':
            DecTreatList.append(count)
    return render_template('admin/feedback/StatTreat.html', title = 'Feedback - Category(Treatment)', max = 20, labels = bar_labels, values = bar_values, JanTreatList = JanTreatList, FebTreatList = FebTreatList, MarTreatList = MarTreatList, AprTreatList = AprTreatList, MayTreatList = MayTreatList, JunTreatList = JunTreatList, JulTreatList = JulTreatList, AugTreatList = AugTreatList, SepTreatList = SepTreatList, OctTreatList = OctTreatList, NovTreatList = NovTreatList, DecTreatList = DecTreatList,
                    jantreatcount = len(JanTreatList), febtreatcount = len(FebTreatList), martreatcount = len(MarTreatList), aprtreatcount = len(AprTreatList), maytreatcount = len(MayTreatList), juntreatcount = len(JunTreatList), jultreatcount = len(JulTreatList), augtreatcount = len(AugTreatList), septreatcount = len(SepTreatList), octtreatcount = len(OctTreatList), novtreatcount = len(NovTreatList), dectreatcount = len(DecTreatList))



####################################################################################
@admin_pages.route('/admin/receipts/view')
@authorize
def list_receipts_admin():
    items = itemcontroller.get_all_receipt()
    return render_template('admin/listing/list_receipts.html',items=items)
####################################################################################
####################################################################################
@admin_pages.route('/admin/receipts/<ruid>/complete')
@authorize
def list_receipts_complete(ruid):
    item = itemcontroller.get_receipt_by_UID(ruid)
    if( not item):
        abort(404)
    item.set_status_complete()
    flash("Status of receipt #" + ruid + " have changed to completed",  "success")
    return redirect(url_for("admin_pages.list_receipts_admin"))
####################################################################################
####################################################################################
@admin_pages.route('/admin/receipts//<ruid>/delivery')
@authorize
def receipts_delivery(ruid):
    item = itemcontroller.get_receipt_by_UID(ruid)
    if( not item):
        abort(404)
    item.set_status_delivery()
    flash("Status of receipt #" + ruid + " have changed to delivery", "success")
    return redirect(url_for("admin_pages.list_receipts_admin"))
####################################################################################
@admin_pages.route('/admin/doctor/createdoctor', methods=['GET', 'POST'])
@authorize
def createdoctor():
    createdoctorForm = CreatedoctorForm()
    if request.method == 'POST' and createdoctorForm.validate():
        doctorsdict = {}
        db = shelve.open('docstorage.db', 'c')

        try:
            doctorsdict = db['doctor']
        except:
            print("Error in retrieving doctor Profile from docstorage.db.")
        f = createdoctorForm.Image.data
        f.save(DOCTORDIR + createdoctorForm.Name.data)
        image_url = DOCTORDIR + createdoctorForm.Name.data
        doctor = Doctor(createdoctorForm.Name.data, createdoctorForm.Specialities.data, createdoctorForm.gender.data, createdoctorForm.Profile.data, createdoctorForm.Status.data,image_url )

        doctorsdict[doctor.get_doctorID()] = doctor
        db['doctor'] = doctorsdict
        db.close()
        return redirect(url_for('admin_pages.retrieveDoctor'))
    return render_template('admin/doctor/createdoctor.html', form=createdoctorForm)

@admin_pages.route('/admin/doctor/retrievedoctor')
@authorize
def retrieveDoctor():
    doctorsDict = {}
    try:
        db = shelve.open('docstorage.db', 'r')
        doctorsDict = db['doctor']
        db.close()
    except:
        pass
    #
    doctorsList = []
    for key in doctorsDict:
        doctor = doctorsDict.get(key)
        doctorsList.append(doctor)

    return render_template('admin/doctor/retrieveDoctor.html', doctorsList=doctorsList, count=len(doctorsList))

@admin_pages.route('/admin/doctor/updatedoctor/<int:id>', methods=['GET','POST'])
@authorize
def updatedoctor(id):
    print(request.form)
    updatedoctorForm = CreatedoctorForm()
    if request.method == 'POST' and updatedoctorForm.validate():
         doctorsDict = {}
         db = shelve.open('docstorage.db', 'w')
         doctorsDict = db['doctor']
         f = updatedoctorForm.Image.data
         f.save(DOCTORDIR + updatedoctorForm.Name.data)
         doctor = doctorsDict.get(id)
         doctor.set_Name(updatedoctorForm.Name.data)
         doctor.set_Specialities(updatedoctorForm.Specialities.data)
         doctor.set_gender(updatedoctorForm.gender.data)
         doctor.set_Profile(updatedoctorForm.Profile.data)
         doctor.set_Status(updatedoctorForm.Status.data)
         doctor.set_Image(DOCTORDIR + updatedoctorForm.Name.data)
         db['doctor'] = doctorsDict
         db.close()

         return redirect(url_for('admin_pages.retrieveDoctor'))

    else:
         print('In here')
         doctorsDict = {}
         db = shelve.open('docstorage.db', 'r')
         doctorsDict = db['doctor']
         db.close()
         doctor = doctorsDict.get(id)
         print(doctor.get_Name())
         updatedoctorForm.Name.data = doctor.get_Name()
         updatedoctorForm.Specialities.data = doctor.get_Specialities()
         updatedoctorForm.gender.data = doctor.get_gender()
         updatedoctorForm.Profile.data = doctor.get_Profile()
         updatedoctorForm.Status.data = doctor.get_Status()

         return render_template('admin/doctor/updatedoctor.html',form=updatedoctorForm)

@admin_pages.route('/admin/doctor/deleteDoctor/<int:id>', methods=['POST'])
@authorize
def deletedoctor(id):
    doctorDict = {}
    db = shelve.open('docstorage.db', 'w')
    doctorDict = db['doctor']

    doctorDict.pop(id)

    db['doctor'] = doctorDict
    db.close()

    return redirect(url_for('admin_pages.retrieveDoctor'))

##################################################################################
##################################################################################
##################################################################################
##################################################################################
##################################################################################
@admin_pages.route('/admin/', methods=['GET', 'POST'])
def admin():
    if(session.get('admin_username')):
        return redirect(url_for("admin_pages.admin_home"))
    adm_login = AdminLogin(request.form)
    if request.method == "POST" and adm_login.validate():

        adminsDict = {}
        db = shelve.open("admins.db", "r")

        try:
            adminsDict = db["Admin"]
        except:
            print("Unable to access shelve")

        username = adm_login.username.data
        password = adm_login.password.data
        for id in adminsDict:
            admin = adminsDict.get(id)
            if admin.get_username() == username:
                if admin.check_password(password):
                    session['admin_logged_in'] = True
                    session['admin_username'] = request.form['username']
                return redirect(url_for("admin_pages.admin_home"))

        flash("Invalid Login, Please try again.", "error")

        return render_template('/admin/admin_login.html', form=adm_login)
    return render_template('/admin/admin_login.html', form=adm_login)

@admin_pages.route('/admin/accounts/admin/create', methods=['GET', 'POST'])
@authorize
def create_admin_accounts():
    createAdmin = create_admin(request.form)
    if request.method == 'POST' and createAdmin.validate():
        adminsDict = {}
        db = shelve.open('admins.db', 'c')
        try:
            adminsDict = db['Admin']
        except:
            print("Error in retrieving Admin from admin.db.")

        admin = Admin(createAdmin.username.data, createAdmin.password.data)
        adminsDict[admin.get_adminID()] = admin
        db['Admin'] = adminsDict

        adminsDict = db['Admin']
        admin = adminsDict[admin.get_adminID()]

        db.close()
        flash("An admin account is created", "success")
        return redirect(url_for('admin_pages.admin'))
    return render_template('/admin/accounts/create_admin_accounts.html', form=createAdmin)





@admin_pages.route('/admin/accounts/list_admins')
@authorize
def list_admin_accounts():
    usersDict = {}
    db = shelve.open('admins.db', 'r')
    usersDict = db['Admin']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        print(user.get_username())
        usersList.append(user)

    return render_template('admin/accounts/list_admin_accounts.html', adminList=usersList, count=len(usersList))

@admin_pages.route('/admin/accounts/admin/<int:id>/delete', methods=['POST'])
@authorize
def delete_admin(id):
    adminsDict = {}
    db = shelve.open('admins.db', 'w')
    adminsDict = db['Admin']

    adminsDict.pop(id)

    db['Admin'] = adminsDict
    db.close()

    return redirect(url_for('list_admin_accounts'))


@admin_pages.route('/admin/accounts/users/list')
@authorize
def list_users_accounts():
    usersDict = {}
    db = shelve.open('users.db', 'r')
    usersDict = db['Users']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)

    return render_template('admin/accounts/list_users_accounts.html', usersList=usersList, count=len(usersList))


@admin_pages.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
@authorize
def updateUser(id):
    updateUserForm = UserRegistration(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        usersDict = {}
        db = shelve.open('users.db', 'w')
        usersDict = db['Users']

        user = usersDict.get(id)
        user.set_email(updateUserForm.email.data)
        user.set_password(updateUserForm.password.data)

        db['Users'] = usersDict
        db.close()

        return redirect(url_for('admin_pages.list_users_accounts'))
    else:
        usersDict = {}
        db = shelve.open('users.db', 'r')
        usersDict = db['Users']
        db.close()

        user = usersDict.get(id)
        updateUserForm.username.data = user.get_username()
        updateUserForm.email.data = user.get_email()

        return render_template('admin/accounts/update_user_accounts.html', form=updateUserForm)


@admin_pages.route('/deleteUser/<int:id>', methods=['POST'])
@authorize
def deleteUser(id):
    usersDict = {}
    db = shelve.open('users.db', 'w')
    usersDict = db['Users']

    usersDict.pop(id)

    db['Users'] = usersDict
    db.close()

    return redirect(url_for('admin_pages.list_users_account'))




################
###############
###
@admin_pages.route('/admin/home', methods=['GET', 'POST'])
@authorize
def admin_home():
    #all the below code displays the coupons that are used and the number of times they are used.
    #get all receipts from itemcontroller
    all_receipts = itemcontroller.get_all_receipt()
    #for counted coupons, insert into it
    all_used = []
    for i in all_receipts:
        #get the coupons from the receipts
        coupon = i.get_coupon()
        if(coupon):
            #if the receipts uses a coupon code
            #gets all the coupons that is in the receipts
            #append it into used_coupons
            all_used.append(coupon.get_couponcode())
        else:
            all_used.append("No Coupon Used")
    all_coupon_used_list = []
    usage_number_list = []
    usedlist = []
    #loop through all used coupons code
    for j in all_used:
        # if couponcode is not in usedlist
        if not (j in usedlist):
            # appends it into all_coupons_used_list
            # this list each has a unique coupon code
            all_coupon_used_list.append(j)
            # count how many instance this coupon code appear in all_used list
            usage_number_list.append(all_used.count(j))
            # appends into used list so we can skip counting the same coupon again
            usedlist.append(j)
    # to display chart, uses chartjs, a javascript library to display the chart.
    return render_template('/admin/Dashboard.html', all_coupons_used_list = all_coupon_used_list, usage_number_list=usage_number_list)


