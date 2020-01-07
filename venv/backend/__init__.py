from flask import url_for, redirect, render_template, Flask, request, flash,session
from flask_uploads import UploadSet, IMAGES,configure_uploads
from backend.admin_url import admin_pages
from backend.settings import *
app = Flask(__name__, template_folder='../templates', static_url_path="/static")



app.register_blueprint(admin_pages)
#main items controller


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




@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "The email is {} and the password is {}".format(email, password)


if __name__ == '__main__':
 app.run(debug=True)


