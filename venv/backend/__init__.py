from flask import url_for, redirect, render_template, Flask, request, flash,session
from backend.forms import new_sales_item,coupon_form,new_package,new_service
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES,configure_uploads
import os
from backend.itemscontroller import *
from flask import send_from_directory
from login.login_controller import *

app = Flask(__name__, template_folder='../templates', static_url_path="/static")


#main items controller
itemcontroller = itemscontroller()
ITEMSDIR= 'static/uploads/items/'
PACKAGEDIR = 'static/uploads/packages/'
SERVICEDIR = 'static/uploads/services/'
UPLOAD_FOLDER = '/uploads/'
app.config['UPLOADED_IMAGES_DEST'] = '/uploads/'
app.config['SECRET_KEY'] = 'THISISNOTASECRET'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PRODUCT'] = UPLOAD_FOLDER , 'product/'

images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/home')
def home():
    return render_template('base.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "The email is {} and the password is {}".format(email, password)



#-------------------------------------------------------------------
#to move to another url blueprint

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return render_template('admin/admin_login.html')
    else:
        return render_template('base.html')



@app.route('/admin/login', methods=['POST'])
def do_admin_login():
    username = request.form['username']
    password = request.form['password']
    login = login_admin("Zarateo", password)
    if(login):
        session['admin_logged_in'] = True
    else:
        flash('Wrong password!')
    return admin()

@app.route('/admin/logout')
def admin_logout():
    session['admin_logged_in'] = False
    return do_admin_login()


# @app.route('/accounts/add/admin')
# def add_admin_accounts():
#     context = {}
#

@app.route('/add/coupons')
def add_coupons():
    context = {}
    cform = coupon_form()
    if request.method == 'POST' and cform.validate():
        new_coupon = itemcontroller.create_and_save_coupon(cform.data)
        if(new_coupon.save()):
            context={
                "message": "You have sucessfully create a new coupon for users to use."
            }
    return render_template('adding/create_coupons.html', form=cform, message=context)




@app.route('/add/services/', methods= ['GET','POST'])
def add_shop_service():
    context = {"message": ""}
    form = new_service()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(SERVICEDIR + filename)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = filename

        item = sfactory.create_items(update_form)
        if (item.save()):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"You have an error."}
    return render_template('adding/create_services.html', form=form, message=context)


@app.route('/add/items/', methods= ['GET','POST'])
def add_shop_item():
    context = {"message": ""}
    form = new_sales_item()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(ITEMSDIR + filename)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = filename

        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error have occured..."}
    return render_template('adding/create_items.html', form=form, message=context)

@app.route('/add/packages/', methods= ['GET','POST'])
def add_shop_package():
    context = {"message": ""}
    form = new_package()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(PACKAGEDIR + filename)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = filename

        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error have occured..."}
    return render_template('adding/create_packages.html', form=form, message=context)



@app.route('/list/sales_items')
def list_sales_items():
    sales = itemcontroller.get_all_sales_items()
    print(sales)
    return render_template('listing/list_sales_items.html', items=sales)


@app.route('/list/items/<int:itemid>/edit/')
def edit_item(itemid):
    return "GG"


@app.route('/list/sales_packages')
def list_sales_packages():
    sales = itemcontroller.get_all_sales_packages()
    return render_template('listing/list_sales_packages.html', items=sales)


@app.route('/list/sales_services')
def list_sales_services():
    sales = itemcontroller.get_all_sales_services()
    return render_template('listing/list_sales_services.html', items=sales)

@app.route('/list/coupons')
def list_coupons():
    sales = itemcontroller.get_all_coupons()
    return render_template('listing/list_sales_coupons.html', items=sales)


if __name__ == '__main__':
 app.run(debug=True)
