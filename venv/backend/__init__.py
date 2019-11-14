from flask import url_for, redirect, render_template, Flask, request
from backend.forms import create_sales_item
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES,configure_uploads
import os
from backend.sales_factory import *
from flask import send_from_directory

app = Flask(__name__, template_folder='../templates', static_url_path="/templates/static")


factory = sales_factory()

UPLOAD_FOLDER = '/uploads/'
app.config['UPLOADED_IMAGES_DEST'] = '/uploads/'
app.config['SECRET_KEY'] = 'THISISNOTAMAMASECRET'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PRODUCT'] = UPLOAD_FOLDER , 'product/'


images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))



@app.route('/')
def home():
    return "gg"
    return render_template('index.html', {})



@app.route('/create/')
def create():
    return "GG"

@app.route('/add/items/', methods= ['GET','POST'])
def add_shop_item():
    context = {"message": ""}
    form = create_sales_item()

    if request.method == 'POST' and form.validate():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save('../../uploads/' + filename)
        # form["image_url"] = filename
        update_form = form.data.copy()
        update_form["image_url"] = filename

        item = factory.create_items(update_form)
        print(item.save())
        context ={"message":"You have created a new item"}
    else:
        print("failed")
        context = {"message": "You did not managed to create the item"}
    return render_template('create_sales.html', form=form, message=context)


@app.route('/list/items')
def list_items():
    sales = factory.get_all_items()
    return render_template('list_sales_items.html', sales=sales)

if __name__ == '__main__':
 app.run(debug=True)
