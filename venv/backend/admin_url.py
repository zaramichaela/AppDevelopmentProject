from flask import Blueprint, abort
from flask import render_template, request, flash,session,redirect, url_for
from backend.forms import *
from functools import wraps
from login.forms import create_admin_account
from backend.settings import *
from login.user_account import *


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
@admin_pages.route('/admin')
def admin():
    print(session.get('admin_logged_in'))
    if not session.get('admin_logged_in'):
        return render_template('admin/admin_login.html')
    else:
        return render_template('admin/admin_base.html')
####################################################################################
@admin_pages.route('/admin/login', methods=['POST'])
def do_admin_login():
    username = request.form['username']
    password = request.form['password']
    if(logincontroller.login_admin(username, password)):
        session['admin_logged_in'] = True
        session['admin_username'] = request.form['username']
    else:
        flash('Wrong credentials!', "error")
    return redirect(url_for("admin_pages.admin"))
####################################################################################
@admin_pages.route('/admin/logout')
@authorize
def admin_logout():
    session['admin_logged_in'] = False
    session['admin_username'] = ""
    return redirect(url_for("admin_pages.admin"))
####################################################################################
@admin_pages.route('/admin/add/coupons', methods= ['GET','POST'])
@authorize
def add_coupons():
    context = {}
    cform = coupon_form()
    if request.method == 'POST' and cform.validate():
        if(itemcontroller.get_coupon_by_UID(cform.UID.data)):
            flash("You have input an UID that exists, please try again.")
            return render_template('admin/adding/create_coupons.html', form=cform, message=context)
        new_coupon = itemcontroller.create_and_save_coupon(cform.data)
        if(new_coupon.save()):
            context = {
                "message": "You have successfully create a new coupon for users to use."
            }
    return render_template('admin/adding/create_coupons.html', form=cform, message=context)
####################################################################################
@admin_pages.route('/admin/add/services/', methods= ['GET','POST'])
@authorize
def add_shop_service():
    context = {"message": ""}
    form = new_service()

    if request.method == 'POST' and form.validate():
        if(itemcontroller.get_service_by_UID(form.UID.data)):
            flash("You have input an UID that exists, please try again.")
            return render_template('admin/adding/create_services.html', form=form, message=context)
        f = form.image.data
        f.save(SERVICEDIR + form.UID.data)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = SERVICEDIR + form.UID.data

        item = itemcontroller.create_and_save_service(update_form)
        if (item.save()):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"An error has occurred."}
    return render_template('admin/adding/create_services.html', form=form, message=context)
####################################################################################
@admin_pages.route('/admin/add/items/', methods= ['GET','POST'])
@authorize
def add_shop_item():
    context = {"message": ""}
    form = new_sales_item()

    if request.method == 'POST' and form.validate():

        if(itemcontroller.get_item_by_UID(form.UID.data)):
            flash("You have input an UID that exists, please try again.")
            return render_template('admin/adding/create_items.html', form=form, message=context)
        f = form.image.data
        f.save(ITEMSDIR + form.UID.data)
        update_form = form.data.copy()
        update_form["image_url"] = ITEMSDIR + form.UID.data
        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error has occurred."}
    return render_template('admin/adding/create_items.html', form=form, message=context)
####################################################################################
@admin_pages.route('/admin/add/packages/', methods= ['GET','POST'])
@authorize
def add_shop_package():
    context = {"message": ""}
    form = new_package()

    if request.method == 'POST' and form.validate():
        if(itemcontroller.get_package_by_UID(form.UID.data)):
            flash("You have input an UID that exists, please try again.")
            return render_template('admin/adding/create_packages.html', form=form, message=context)
        f = form.image.data
        f.save(PACKAGEDIR + form.UID.data)
        update_form = form.data.copy()
        update_form["image_url"] = PACKAGEDIR + form.UID.data

        item = itemcontroller.create_and_save_package(update_form)
        if (item):
            context ={"message":"You have created a new package"}
        else:
            context ={"error":"A error has occurred."}
    return render_template('admin/adding/create_packages.html', form=form, message=context)
####################################################################################
@admin_pages.route('/admin/list/items')
@authorize
def list_sales_items():
    sales = itemcontroller.get_all_sales_items()
    return render_template('admin/listing/list_sales_items.html', items=sales)
####################################################################################
@admin_pages.route('/admin/list/sales_packages')
@authorize
def list_sales_packages():
    sales = itemcontroller.get_all_sales_packages()
    return render_template('admin/listing/list_sales_packages.html', items=sales)
####################################################################################
@admin_pages.route('/admin/list/sales_services')
@authorize
def list_sales_services():
    sales = itemcontroller.get_all_sales_services()
    return render_template('admin/listing/list_sales_services.html', items=sales)
####################################################################################
@admin_pages.route('/admin/list/coupons')
@authorize
def list_coupons():
    sales = itemcontroller.get_all_coupons()
    return render_template('admin/listing/list_coupons.html', items=sales)
####################################################################################


#########################################################################################
############### deleting items and objects ########################################
#########################################################################################

@admin_pages.route('/admin/list/items/<itemid>/delete/', methods= ['GET','POST'])
@authorize
def delete_sales_item(itemid):
    context = {"message": ""}
    item = itemcontroller.get_item_by_UID(itemid)
    if(not item):
        abort(404)
    flag = itemcontroller.remove_sales_item(item)
    if flag:
        flash("You have succeed in removing item " + item.get_UID(), "success")
    else:
        flash("There's been a error removing " + item.get_UID(), "error")
    return redirect(url_for("admin_pages.list_sales_items"))
####################################################################################
@admin_pages.route('/admin/list/items/<itemid>/invalidate/', methods= ['GET','POST'])
@authorize
def invalidate_sales_item(itemid):
    context = {"message": ""}
    item = itemcontroller.get_item_by_UID(itemid)
    if(not item):
        abort(404)
    flag = True
    if(item.get_available_flag()):
        flag = False
    else:
        flag = True
    item.set_available_flag(flag)
    if flag:
        flash("You have set the item " + item.get_UID() + " to available", "success")
    else:
        flash("You have set the item " + item.get_UID() + " to unavailable", "success")
    return redirect(url_for("admin_pages.list_sales_items"))
####################################################################################
@admin_pages.route('/admin/list/package/<packageid>/delete/', methods= ['GET','POST'])
@authorize
def delete_package(packageid):
    context = {"message": ""}
    item = itemcontroller.get_package_by_UID(packageid)
    if(not item):
        abort(404)
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
    context = {"message": ""}
    item = itemcontroller.get_package_by_UID(packageid)
    if(not item):
        abort(404)
    flag = True
    if(item.get_available_flag()):
        flag = False
    else:
        flag = True
    item.set_available_flag(flag)
    if flag:
        flash("You have set the package #" + item.get_UID() + " to available", "success")
    else:
        flash("You have set the package #" + item.get_UID() + " to unavailable", "success")
    return redirect(url_for("admin_pages.list_sales_packages"))
####################################################################################
@admin_pages.route('/admin/list/service/<serviceid>/delete/', methods= ['GET','POST'])
@authorize
def delete_service(serviceid):
    context = {"message": ""}
    item = itemcontroller.get_service_by_UID(serviceid)
    if(not item):
        abort(404)
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
    context = {"message": ""}
    item = itemcontroller.get_package_by_UID(serviceid)
    if(not item):
        abort(404)
    flag = True
    if(item.get_available_flag()):
        flag = False
    else:
        flag = True
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
    context = {"message": ""}
    item = itemcontroller.get_coupon_by_UID(couponid)
    if(not item):
        abort(404)
    flag = itemcontroller.remove_sales_coupon(item)
    if flag:
        flash("You have succeed in removing item " + item.get_UID(),"success")
    else:
        flash("There's been a error removing " + item.get_UID(), "error")
    return redirect(url_for("admin_pages.list_coupons"))
####################################################################################


#########################################################################################
############### editing each objects information ########################################
#########################################################################################

@admin_pages.route('/admin/list/items/<itemid>/edit/', methods= ['GET','POST'])
@authorize
def edit_item(itemid):
    context = {"message": ""}
    item = itemcontroller.get_item_by_UID(itemid)
    if(not item):
        abort(404)
    form = edit_sales_item()
    if request.method == 'POST' and form.validate_on_submit():
        file_ = request.files["image"]
        if(file_):
            file_.save(ITEMSDIR+item.get_UID())
        update_form = form.data.copy()
        update_form["UID"] = item.get_UID()
        update_form["image_url"] = ITEMSDIR + item.get_UID()
        itemcontroller.remove_sales_item(item)
        item2 = itemcontroller.create_and_save_item(update_form)
        if (item2):
            flash("You have updated the item "+ item.get_UID() +" information", "success")
            return redirect(url_for("admin_pages.list_sales_items"))
        else:
            context ={"error":"A error have occurred..."}
            itemcontroller.all_items.append(item)
            item.save()
    else:
            form.name.data = item.get_name()
            form.category.data = item.get_category()
            form.discount.data = item.get_discount()
            form.description.data = item.get_description()
            form.price.data = item.get_price()
            form.stocks.data = item.get_stocks()
    return render_template('admin/editing/edit_items.html', form=form, message=context, item=item)
####################################################################################

@admin_pages.route('/admin/list/packages/<packageid>/edit/', methods= ['GET','POST'])
@authorize
def edit_package(packageid):
    context = {"message": ""}
    item = itemcontroller.get_package_by_UID(packageid)
    if(not item):
        abort(404)
    form = edit_package_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
        file_ = request.files["image"]
        if(file_):
            file_.save(PACKAGEDIR+item.get_UID())
        update_form = form.data.copy()
        update_form["UID"] = item.get_UID()
        update_form["image_url"] = PACKAGEDIR +item.get_UID()
        itemcontroller.remove_sales_package(item)
        item2 = itemcontroller.create_and_save_package(update_form)
        if (item2):
            flash("You have updated the package "+ item2.get_UID() +" information", "success")
            return redirect(url_for("admin_pages.list_sales_packages"))
        else:
            context ={"error":"A error have occurred..."}
            itemcontroller.all_packages(item)
            item.save()
    else:
            form.name.data = item.get_name()
            form.discount.data = item.get_discount()
            form.description.data = item.get_description()
            form.price.data = item.get_price()
            form.expiry_duration.data = item.get_expiry_duration()
            form.sessions.data = item.get_sessions()

    return render_template('admin/editing/edit_packages.html', form=form, message=context, item=item)
####################################################################################
@admin_pages.route('/admin/list/services/<serviceid>/edit/', methods= ['GET','POST'])
@authorize
def edit_service(serviceid):
    context = {"message": ""}
    item = itemcontroller.get_service_by_UID(serviceid)
    if(not item):
        abort(404)
    form = edit_service_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():

        file_ = request.files["image"]
        if(file_):
            file_.save(SERVICEDIR+item.get_UID())

        update_form = form.data.copy()
        update_form["UID"] = item.get_UID()
        update_form["image_url"] = SERVICEDIR + item.get_UID()

        item2 = itemcontroller.create_and_save_service(update_form)
        itemcontroller.remove_sales_service(item)
        if (item2):
            flash("You have updated the service "+ item2.get_UID() +" information", "success")
            return redirect(url_for("admin_pages.list_sales_services"))
        else:
            context ={"error":"A error have occurred..."}
            itemcontroller.all_services(item)
            item.save()
    else:
        form.name.data = item.get_name()
        form.discount.data = item.get_discount()
        form.description.data = item.get_description()
        form.price.data = item.get_price()
    return render_template('admin/editing/edit_services.html', form=form, message=context, item=item)
####################################################################################
@admin_pages.route('/admin/list/coupons/<couponid>/edit/', methods= ['GET','POST'])
@authorize
def edit_coupon(couponid):
    context = {"message": ""}
    item = itemcontroller.get_coupon_by_UID(couponid)
    if(not item):
        abort(404)
    form = edit_coupon_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
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
    return render_template('admin/editing/edit_coupons.html', form=form, message=context, item=item)
####################################################################################
@admin_pages.route('/admin/accounts/add', methods= ['GET','POST'])
@authorize
def create_admin_accounts():
    context = {}
    form = create_admin_account()
    if request.method == 'POST' and form.validate():
        success_flag = logincontroller.add_admin_account(form.username.data, form.password.data)
        if (not success_flag):
            flash("Error, you cannot create an account", "error")
        else:
            flash("Admin account created.", "success")
        form = create_admin_account()
    return render_template('admin/accounts/create_admin_accounts.html', form=form, message=context)
####################################################################################
@admin_pages.route('/admin/accounts/admin/view')
@authorize
def list_admin_accounts():
    context = {}
    items = logincontroller.get_all_admins()
    return render_template('admin/accounts/list_admin_accounts.html',items=items)
####################################################################################
@admin_pages.route('/admin/accounts/admins/<username>/delete/')
@authorize
def del_admin_account(username):
    flag = logincontroller.find_admin_username(username)
    if flag:
        a = logincontroller.delete_admin_account(username)
        flash("You have deleted the admin user " + username, "success")
    else:
        flash("an error have occurred, please try again", "error")
        abort(404)
    return redirect(url_for("admin_pages.list_admin_accounts"))
####################################################################################
@admin_pages.route('/admin/accounts/admin/changepassword/', methods= ['GET','POST'])
@authorize
def change_admin_password():
    context={}
    item = logincontroller.find_user_username(session['admin_username'])
    form = edit_admin_account()
    if(request.method == "POST" and form.validate()):
        username = session["admin_username"]
        logincontroller.change_admin_password(username, form.old_password.data, form.password.data)
    return render_template('admin/accounts/edit_admin_accounts.html',form =form,message=context)
####################################################################################
@admin_pages.route('/admin/accounts/users/view')
@authorize
def list_users_accounts():
    context = {}
    items = logincontroller.get_all_users()
    return render_template('admin/accounts/list_users_accounts.html',items=items)
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
        flash("an error have occurred, please try again", "error")
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
            return render_template('admin/suppliers/create_suppliers.html', form=form)

        success_flag = suppliercontroller.create_and_save_supplier_order(form.data)
        if (not success_flag):
            flash("Error, you cannot list a new supplier", "error")
        else:
            flash("A new supplier has been listed", "success")
            return redirect(url_for("admin_pages.list_suppliers_orders"))
    return render_template('admin/suppliers/create_suppliers_orders.html', form=form)
####################################################################################
@admin_pages.route('/admin/suppliersorders/<orderid>/cancel', methods= ['GET','POST'])
@authorize
def cancel_suppliers_order(orderid):
    item = suppliercontroller.get_suppliers_orders_by_UID(orderid)
    if(not item):
        abort(404)
    item.set_progress("cancelled")
    item.save()
    flash("you have cancelled the order.", "success")
    return redirect(url_for("admin_pages.list_suppliers_orders"))
####################################################################################
@admin_pages.route('/admin/suppliersorders/<orderid>/received', methods= ['GET','POST'])
@authorize
def received_suppliers_order(orderid):
    item = suppliercontroller.get_suppliers_orders_by_UID(orderid)
    if(not item):
        abort(404)
    suppliercontroller.remove_sales_supplier_order(item)
    item.set_progress("received")
    item.save()
    suppliercontroller.add_supplier_order(item)
    flash("you have received the order.", "success")
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
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
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
    return render_template('admin/feedback/StatGraph.html', title = 'Feedback - Statistics(Graph)', max = 20, labels = bar_labels, values = bar_values, TotalList = TotalList, JanList = JanList, FebList = FebList, MarList = MarList, AprList = AprList, MayList = MayList, JunList = JunList, JulList = JulList, AugList = AugList, SepList = SepList, OctList = OctList, NovList = NovList, DecList = DecList,
                           count = len(TotalList), jancount = len(JanList), febcount = len(FebList), marcount = len(MarList), aprcount = len(AprList), maycount = len(MayList), juncount = len(JunList), julcount = len(JulList), augcount = len(AugList), sepcount = len(SepList), octcount = len(OctList), novcount = len(NovList), deccount = len(DecList))
####################################################################################
