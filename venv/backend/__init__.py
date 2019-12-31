from flask import url_for, redirect, render_template, Flask, request
"""
from backend.forms import new_sales_item,coupon_form,new_package,new_service
"""
from werkzeug.utils import secure_filename
"""
from flask_uploads import UploadSet, IMAGES,configure_uploads
"""
import os
"""
from backend.itemscontroller import *
"""
from flask import send_from_directory

app = Flask(__name__, template_folder='../templates', static_url_path="/templates/static")
"""
#main items controller
itemcontroller = itemscontroller()
"""
UPLOAD_FOLDER = '/uploads/'
app.config['UPLOADED_IMAGES_DEST'] = '/uploads/'
app.config['SECRET_KEY'] = 'THISISNOTASECRET'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PRODUCT'] = UPLOAD_FOLDER , 'product/'

"""
images = UploadSet('images', IMAGES)
"""
"""
configure_uploads(app, (images,))
"""


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

@app.route('/add/coupons')
def add_coupons():
    context = {}
    cform = coupon_form()
    if request.method == 'POST' and cform.validate():
        new_coupon = itemcontroller.create_and_save_coupon(cform.data)
        print(new_coupon.save())
    return render_template('create_coupons.html', form=cform, message=context)




@app.route('/add/services/', methods= ['GET','POST'])
def add_shop_service():
    context = {"message": ""}
    form = new_service()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save('../../uploads/services/' + filename)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = filename

        item = sfactory.create_items(update_form)
        if (item.save()):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"You have an error."}
    return render_template('create_sales/create_services.html', form=form, message=context)


@app.route('/add/items/', methods= ['GET','POST'])
def add_shop_item():
    context = {"message": ""}
    form = new_sales_item()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save('../../uploads/items/' + filename)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = filename

        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error have occured..."}
    return render_template('create_sales/create_items.html', form=form, message=context)

@app.route('/add/packages/', methods= ['GET','POST'])
def add_shop_package():
    context = {"message": ""}
    form = new_package()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save('../../uploads/packages/' + filename)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = filename

        item = itemcontroller.create_and_save_item(update_form)
        if (item):
            context ={"message":"You have created a new item"}
        else:
            context ={"error":"A error have occured..."}
    return render_template('create_sales/create_packages.html', form=form, message=context)



@app.route('/list/items')
def list_items():
    sales = sfactory.get_all_items()
    return render_template('listing/list_sales_items.html', sales=sales)

@app.route('/list/items/<int:itemid>/edit/')
def edit_item(itemid):
    return "GG"


if __name__ == '__main__':
 app.run(debug=True)
