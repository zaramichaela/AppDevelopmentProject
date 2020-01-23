from flask import url_for, redirect, render_template, Flask, request, flash, session,abort
from flask_uploads import UploadSet, IMAGES,configure_uploads
# import shelve
from backend.admin_url import admin_pages
from backend.settings import *
from flask_login import LoginManager
from login.forms import customer_registration
from login.user_account import user_account


app = Flask(__name__, template_folder='../templates', static_url_path="/static")

login = LoginManager(app)
app.register_blueprint(admin_pages) #split url to 2 files: admin_url and init
#main items controller


UPLOAD_FOLDER = '/uploads/'
app.config['UPLOADED_IMAGES_DEST'] = '/uploads/'
app.config['SECRET_KEY'] = 'THISISNOTASECRET'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PRODUCT'] = UPLOAD_FOLDER, 'product/'

images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shop')
def shop():
    sales_items = itemcontroller.get_all_sales_items()
    return render_template('users/shop.html', items = sales_items)

@app.route('/shop/items/<itemuid>')
def shop_item(itemuid):
    item = itemcontroller.get_item_by_UID(itemuid)
    if(not item):
        abort(404)
    return render_template('users/item.html', item = item)

@app.route('/cart/<itemuid>/add', methods=['POST'])
def add_item_to_cart(itemuid):
    num = 0
    item = itemcontroller.get_item_by_UID(itemuid)
    if(not item):
        abort(404)
    if not session.get('cart'):
        session['cart'] = []
    flag = False
    for i in session['cart']:
        if(itemuid == i['itemuid']):
            quantity = request.form['quantity']
            i['quantity'] += quantity
            flag = True
            break
    if(not flag):
        appenditem = dict()
        appenditem['itemuid'] = itemuid
        quantity = request.form['quantity']
        if(int(quantity) <= item.get_stocks()):
            appenditem['quantity'] = quantity
            session['cart'].append(appenditem)
            flash("item added to cart.", "success")
    else:
        flash("item not added to cart, quantity exceeds stocks available.", "error")
    return redirect(url_for("shop_item", itemuid=itemuid))

@app.route('/cart')
def cart():
    #need to input coupon code,removing of items and others
    items = session.get("cart")
    cart_list = []
    if(items):
        total_price = 0
        for i in items:
            cart_item = dict()
            cart_item['item'] = itemcontroller.get_item_by_UID(i['itemuid'])
            if(cart_item['item']):
                cart_item['quantity'] = i['quantity']
                cart_item['total'] = int(i['quantity']) * cart_item['item'].price_after_discount()
                cart_list.append(cart_item)
                total_price = total_price + cart_item['total']

        return render_template('cart.html', cart_items=cart_list, total_price=total_price)
    else:
        return render_template('cart.html', cart_items=[])


@app.route('/cart/clear')
def del_cart():
    session.pop('cart', None)
    return redirect(url_for("cart"))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/login/validation', methods=['POST'])
def do_user_login():
    username = request.form['username']
    password = request.form['password']
    user = logincontroller.login_user(username, password)
    if user:
        session['logged_in'] = True
        session['logged_in_user'] = username

    return redirect(url_for("login"))



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = customer_registration()
    if(logincontroller.find_user_username(form.username.data)):
        flash("Username exists, please  choose another.", "error")
    if request.method == 'POST' and form.validate():

        flag = logincontroller.create_user_account(form.username.data, form.password.data, form.email.data)
        if(flag):
            flash("You have registered, please login", "success")
            return redirect(url_for('login'))
        else:
            flash("you have failed to register, something went wrong, try again", "error")

    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session['logged_in_user'] = ''
    return redirect(url_for('home'))



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

# @app.route('/cart')
# def cart():
#     usersDict = {}
#     db = shelve.open('storage.db', 'r')
#     usersDict = db['ShoppingCart']
#     db.close()
#
#     accountList = []
#     for key in accountDict:
#         account = accountDict.get(key)
#         accountList.append(user)
#
#     return render_template('RetrieveAccount.html', accountList = accountList, count =len(accountList))
#
#     usersList = []
#    #create user object 1, store in variable u1
#     u1 = ShoppingCart.ShoppingCart("Medicine1", "D11", 4.00, 1)
#     usersList.append(u1)
#    #create user object 2, store in variable u2
#     u2 = ShoppingCart.ShoppingCart("Medicine2", "D12", 2.00, 3)
#     usersList.append(u2)
#     u3 = ShoppingCart.ShoppingCart("Medicine3", "D13", 1.00, 2)
#     usersList.append(u3)
#
#     for key in usersDict:
#         user = usersDict.get(key)
#         usersList.append(user)
#
#     for u in userList:
#         print(u.get_productName(), u.get_ID(), u.get_price(), u.get_quantity())
#         print(u.computeTotalProduct())
#     return render_template("cart.html", usersList=usersList, count=len(usersList))


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




@app.route('/account/changepassword', methods = ['GET', 'POST'])
def change_pass():

    return render_template("base.html")








if __name__ == '__main__':
 app.run(debug=True)
