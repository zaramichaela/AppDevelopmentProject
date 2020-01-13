from flask import Blueprint, abort
from flask import render_template, request, flash,session,redirect, url_for
from backend.forms import *

from functools import wraps
from login.forms import create_admin_account
from backend.settings import *
from login.user_account import *

admin_pages = Blueprint('admin_pages', __name__, template_folder='templates')




def authorize(f):
    """
    Wrapper function to make sure that the user is logged in as admin
    before being able to access the pages that the wrapper protects.
    e.g. you need to login as admin
    otherwise you wont be able to access links like /admin/add/coupons and etc...
    """
    @wraps(f)
    def decorated_function(*args, **kws):
        if(session.get('admin_logged_in')):
            return f(*args, **kws)
        else:
            flash("You must log in as an admin first.")
            return redirect(url_for("admin_pages.admin"))
    return decorated_function


@admin_pages.route('/admin')
def admin():
    print(session.get('admin_logged_in'))
    if not session.get('admin_logged_in'):
        return render_template('admin/admin_login.html')
    else:
        return render_template('admin/base.html')



@admin_pages.route('/admin/login', methods=['POST'])
def do_admin_login():
    username = request.form['username']
    password = request.form['password']
    if(logincontroller.login_admin(username, password)):
        session['admin_logged_in'] = True
        session['admin_username'] = request.form['username']
    else:
        flash('Wrong credentials!')
    return redirect(url_for("admin_pages.admin"))

@admin_pages.route('/admin/logout')
@authorize
def admin_logout():
    session['admin_logged_in'] = False
    session['admin_username'] = ""
    return redirect(url_for("admin_pages.admin"))


# @app.route('/accounts/add/admin')
# def add_admin_accounts():
#     context = {}
#

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
            context={
                "message": "You have successfully create a new coupon for users to use."
            }
    return render_template('admin/adding/create_coupons.html', form=cform, message=context)




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
            context ={"error":"an error have occurred."}
    return render_template('admin/adding/create_services.html', form=form, message=context)


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
            context ={"error":"A error have occurred..."}
    return render_template('admin/adding/create_items.html', form=form, message=context)

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
            context ={"error":"A error have occurred..."}
    return render_template('admin/adding/create_packages.html', form=form, message=context)



@admin_pages.route('/admin/list/items')
@authorize
def list_sales_items():
    sales = itemcontroller.get_all_sales_items()
    print(sales)
    return render_template('admin/listing/list_sales_items.html', items=sales)


@admin_pages.route('/admin/list/sales_packages')
@authorize
def list_sales_packages():
    sales = itemcontroller.get_all_sales_packages()
    return render_template('admin/listing/list_sales_packages.html', items=sales)



@admin_pages.route('/admin/list/sales_services')
@authorize
def list_sales_services():
    sales = itemcontroller.get_all_sales_services()
    return render_template('admin/listing/list_sales_services.html', items=sales)

@admin_pages.route('/admin/list/coupons')
@authorize
def list_coupons():
    sales = itemcontroller.get_all_coupons()
    return render_template('admin/listing/list_coupons.html', items=sales)


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


@admin_pages.route('/admin/list/package/<packageid>/delete/', methods= ['GET','POST'])
@authorize
def delete_package(packageid):
    context = {"message": ""}
    item = itemcontroller.get_package_by_UID(packageid)
    if(not item):
        abort(404)
    flag = itemcontroller.remove_sales_package(item)
    if flag:
        flash("You have succeed in removing item " + item.get_UID(), "success")
    else:
        flash("There's been a error removing " + item.get_UID(), "error")
    return redirect(url_for("admin_pages.list_sales_packages"))


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
    form = edit_sales_item(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate_on_submit():
        f = form.image.data
        print(os.getcwd())
        print(os.path.exists(PACKAGEDIR + form.UID.data))
        if(f):
            os.remove(ITEMSDIR + form.UID.data)
            f.save(ITEMSDIR + form.UID.data)
        else:
            os.rename(ITEMSDIR+itemid,ITEMSDIR+form.UID.data)
        update_form = form.data.copy()
        update_form["image_url"] = ITEMSDIR + form.UID.data
        itemcontroller.remove_sales_item(item)
        item2 = itemcontroller.create_and_save_item(update_form)
        if (item2):
            context ={"message":"You have created a new item"}
            flash("You have updated the item "+ item.get_UID() +" information")
            return redirect(url_for("admin_pages.list_sales_items"))
        else:
            context ={"error":"A error have occured..."}
            itemcontroller.all_items.append(item)
            item.save()
    return render_template('admin/editing/edit_items.html', form=form, message=context, item=item)


@admin_pages.route('/admin/list/packages/<packageid>/edit/', methods= ['GET','POST'])
@authorize
def edit_package(packageid):
    context = {"message": ""}
    item = itemcontroller.get_package_by_UID(packageid)
    if(not item):
        abort(404)
    form = edit_package_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
        f = form.image.data
        if(f):
            if os.path.exists(PACKAGEDIR + form.UID.data):
                os.remove(PACKAGEDIR + form.UID.data)
        else:
            os.rename(PACKAGEDIR+packageid,PACKAGEDIR+form.UID.data)

        update_form = form.data.copy()
        update_form["image_url"] = PACKAGEDIR + form.UID.data
        itemcontroller.remove_sales_package(item)
        item2 = itemcontroller.create_and_save_package(update_form)
        if (item2):
            context ={"message":"You have edited and updated the package"}
            flash("You have updated the package "+ item2.get_UID() +" information")
            return redirect(url_for("admin_pages.list_sales_packages"))
        else:
            context ={"error":"A error have occurred..."}
            itemcontroller.all_packages(item)
            item.save()
    return render_template('admin/editing/edit_packages.html', form=form, message=context, item=item)


@admin_pages.route('/admin/list/services/<serviceid>/edit/', methods= ['GET','POST'])
@authorize
def edit_service(serviceid):
    context = {"message": ""}
    item = itemcontroller.get_service_by_UID(serviceid)
    if(not item):
        abort(404)
    form = edit_service_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
        f = form.image.data
        if(f):
            if os.path.exists(SERVICEDIR + form.UID.data):
                os.remove(SERVICEDIR + form.UID.data)
        else:
            os.rename(SERVICEDIR+serviceid,SERVICEDIR+form.UID.data)

        update_form = form.data.copy()
        update_form["image_url"] = SERVICEDIR + form.UID.data

        item2 = itemcontroller.create_and_save_service(update_form)
        itemcontroller.remove_sales_service(item)
        if (item2):
            context ={"message":"You have edited and updated the service"}

            flash("You have updated the service "+ item2.get_UID() +" information")
            return redirect(url_for("admin_pages.list_sales_services"))
        else:
            context ={"error":"A error have occurred..."}
            itemcontroller.all_services(item)
            item.save()
    return render_template('admin/editing/edit_services.html', form=form, message=context, item=item)


@admin_pages.route('/admin/list/coupons/<couponid>/edit/', methods= ['GET','POST'])
@authorize
def edit_coupon(couponid):
    context = {"message": ""}
    item = itemcontroller.get_coupon_by_UID(couponid)
    if(not item):
        abort(404)
    form = coupon_form(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
        itemcontroller.remove_sales_coupon(item)

        item2 = itemcontroller.create_and_save_coupon(form.data)
        if (item2):
            flash("You have updated the coupon "+ item.get_UID() +" information")
            return redirect(url_for("admin_pages.list_coupons"))
        else:
            context ={"error":"A error have occurred..."}
            itemcontroller.all_coupons(item)
            item.save()
    return render_template('admin/editing/edit_coupons.html', form=form, message=context, item=item)




@admin_pages.route('/admin/accounts/add', methods= ['GET','POST'])
@authorize
def create_admin_accounts():
    context = {}
    form = create_admin_account()
    if request.method == 'POST' and form.validate():
        success_flag = logincontroller.add_admin_account(form.username.data, form.password.data)
        if (not success_flag):
            flash("Error, you cannot create an account")
        else:
            context["message"] = "Admin account created."
        form = create_admin_account()
    return render_template('admin/accounts/create_admin_accounts.html', form=form, message=context)

@admin_pages.route('/admin/accounts/admin/view')
@authorize
def list_admin_accounts():
    context = {}
    items = logincontroller.get_all_admins()
    return render_template('admin/accounts/list_admin_accounts.html',items=items)

@admin_pages.route('/admin/accounts/admins/<username>/delete/')
@authorize
def del_admin_account(username):
    flag = logincontroller.find_user_username(username)
    if(not flag):
        abort(404)
    if flag:
        flash("You have deleted the admin user " + username, "success")
        logincontroller.delete_admin_account(username)
    else:
        flash("an error have occurred, please try again", "error")
    return redirect(url_for("admin_pages.list_admin_accounts"))

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


@admin_pages.route('/admin/accounts/users/view')
@authorize
def list_users_accounts():
    context = {}
    items = logincontroller.get_all_users()
    return render_template('admin/accounts/list_users_accounts.html',items=items)



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
