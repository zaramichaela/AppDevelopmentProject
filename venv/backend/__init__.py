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
app.config['UPLOAD_PRODUCT'] = UPLOAD_FOLDER, 'product/'

images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


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
        context = {"message": "You did not manage to create the item"}
    return render_template('create_sales.html', form=form, message=context)


@app.route('/list/items')
def list_items():
    sales = factory.get_all_items()
    return render_template('list_sales_items.html', sales=sales)

@app.route('/AccountCreation', methods = ['GET', 'POST'])
def createAccount():
    createAccountForm = CreateAccountForm(request.form)
    if request.method == 'POST' and createAccountForm.validate():
        AccountDict = {}
        db = shelve.open('storage.db', 'c')

        try:
            AccountDict = db['Users']
        except:
            print("Error in retrieving Users from storage.db")

        account = Account.Account(createAccountForm.firstName.data, createAccountForm.lastName.data, createAccountForm.gender.data)
        AccountDict[account.account.get_userID()] = account
        db['Account'] = AccountDict
        db.close()

        return redirect(url_for('RetrieveAccount'))
    return render_template('AccountCreation.html', form=createAccountForm)

@app.route('/RetrieveAccount')
def retrieveAccount():
    accountDict = {}

@app.route('/cart')
def cart():
    usersDict = {}
    db = shelve.open('storage.db', 'r')
    usersDict = db['ShoppingCart']
    db.close()

    accountList = []
    for key in accountDict:
        account = accountDict.get(key)
        accountList.append(user)

    return render_template('RetrieveAccount.html', accountList = accountList, count =len(accountList))

    usersList = []
   #create user object 1, store in variable u1
    u1 = ShoppingCart.ShoppingCart("Medicine1", "D11", 4.00, 1)
    usersList.append(u1)
   #create user object 2, store in variable u2
    u2 = ShoppingCart.ShoppingCart("Medicine2", "D12", 2.00, 3)
    usersList.append(u2)
    u3 = ShoppingCart.ShoppingCart("Medicine3", "D13", 1.00, 2)
    usersList.append(u3)

    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)

    for u in userList:
        print(u.get_productName(), u.get_ID(), u.get_price(), u.get_quantity())
        print(u.computeTotalProduct())
    return render_template("cart.html", usersList=usersList, count=len(usersList))


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "The email is {} and the password is {}".format(email, password)

# To add custom error 404 page
@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404

# To add custom error 403 page
@app.errorhandler(403)
def not_found(e):
    return render_template('error_pages/403.html'), 403

# To add custom error 410 page
@app.errorhandler(410)
def not_found(e):
    return render_template('error_pages/410.html'), 410

# To add custom error 500 page
@app.errorhandler(500)
def not_found(e):
    return render_template('error_pages/500.html'), 500

if __name__ == '__main__':
 app.run(debug=True)
