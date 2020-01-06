from flask import Blueprint, abort
from flask import render_template, request, flash,session,redirect, url_for
from jinja2 import TemplateNotFound
from backend.forms import new_sales_item,coupon_form,new_package,new_service
from werkzeug.utils import secure_filename

from functools import wraps
from login.forms import create_admin_account
from backend.settings import *

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
    else:
        flash('Wrong credentials!')
    return redirect(url_for("admin_pages.admin"))

@admin_pages.route('/admin/logout')
@authorize
def admin_logout():
    session['admin_logged_in'] = False
    return redirect(url_for("admin_pages.admin"))


# @app.route('/accounts/add/admin')
# def add_admin_accounts():
#     context = {}
#

@admin_pages.route('/admin/add/coupons')
@authorize
def add_coupons():
    context = {}
    cform = coupon_form()
    if request.method == 'POST' and cform.validate():
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
        f = form.image.data
        f.save(SERVICEDIR + form.UID.data)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = SERVICEDIR + form.UID.data

        item = sfactory.create_items(update_form)
        if (item.save()):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"You have an error."}
    return render_template('admin/adding/create_services.html', form=form, message=context)


@admin_pages.route('/admin/add/items/', methods= ['GET','POST'])
@authorize
def add_shop_item():
    context = {"message": ""}
    form = new_sales_item()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        f.save(ITEMSDIR + form.UID.data)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = ITEMSDIR + form.UID.data

        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error have occured..."}
    return render_template('admin/adding/create_items.html', form=form, message=context)

@admin_pages.route('/admin/add/packages/', methods= ['GET','POST'])
@authorize
def add_shop_package():
    context = {"message": ""}
    form = new_package()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        f.save(PACKAGEDIR + form.UID.data)
        update_form = form.data.copy()
        update_form["image_url"] = PACKAGEDIR + form.UID.data

        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error have occured..."}
    return render_template('admin/adding/create_packages.html', form=form, message=context)



@admin_pages.route('/admin/list/items')
@authorize
def list_sales_items():
    sales = itemcontroller.get_all_sales_items()
    print(sales)
    return render_template('admin/listing/list_sales_items.html', items=sales)



#########################################################################################
############### editing each objects information ########################################
#########################################################################################

@admin_pages.route('/admin/list/items/<itemid>/edit/')
@authorize
def edit_item(itemid):
    context = {"message": ""}
    item = itemcontroller.get_item_by_UID(itemid)
    if(not item):
        abort(404)
    form = new_sales_item(formdata=request.form, obj=item)

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(ITEMSDIR + filename)
        update_form = form.data.copy()
        update_form["image_url"] = ITEMDIR + filename

        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error have occured..."}
    return render_template('admin/adding/create_items.html', form=form, message=context)


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




@admin_pages.route('/admin/accounts/add', methods= ['GET','POST'])
@authorize
def create_admin_accounts():
    context = {}
    form = create_admin_account()
    if request.method == 'POST' and form.validate():
        success_flag = logincontroller.add_admin_account(form.password.data, form.password.data)
        if (not success_flag):
            pass
        else:
            context["message"] = "Account created."

    return render_template('admin/accounts/create_admin_accounts.html', form=form, message=context)

