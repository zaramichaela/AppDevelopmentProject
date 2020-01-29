from flask import url_for, redirect, render_template, Flask, request, flash, session,abort
from flask_uploads import UploadSet, IMAGES,configure_uploads
import shelve, Feedback
from datetime import date
from backend.admin_url import admin_pages
from backend.settings import *
from flask_login import LoginManager
from login.forms import customer_registration
from login.user_account import user_account
from backend.forms import checkout_form
from backend.user_details import *
# from Forms import CreateFeedbackForm, UpdateFeedbackForm


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

@app.route('/contactus', methods=['GET'])
def contact():
    return render_template("users/receipt.html")

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
            quantity = int(request.form['quantity'])
            i['quantity'] += (quantity)
            if(i['quantity'] > itemcontroller.get_item_by_UID(itemuid).get_stocks()):
                flash("Error, item quantity cannot exceed amount of stocks.", "error")

            flag = True
            flash("item already exists in cart, increase quantity by " +  str(quantity), "success")
            break
    if(not flag):
        appenditem = dict()
        appenditem['itemuid'] = itemuid
        quantity = int(request.form['quantity'])
        if(int(quantity) <= item.get_stocks()):
            appenditem['quantity'] = quantity
            session['cart'].append(appenditem)
            flash("item added to cart.", "success")
        else:
            flash("item not added to cart, quantity exceeds stocks available.", "error")
    return redirect(url_for("shop_item", itemuid=itemuid))

@app.route('/cart/delete/<itemuid>')
def del_cart_item(itemuid):
    items = session.get("cart")
    remove = None
    for i in items:
        if(itemuid ==  i['itemuid']):
            remove = i
    items.remove(remove)
    session['cart'] = items
    return redirect(url_for("cart"))

@app.route('/cart' , methods=['POST', 'GET'])
def cart():
    #need to input coupon code,removing of items and others
    items = session.get("cart")
    cart_list = []
    code = ''
    discount = 0.00
    total_amount = 0 # every item add together - discount
    if(items):
        subtotal_price = 0 #all items
        if request.method == 'POST' and request.form.get('quantity'):
            #get value from the individual form of the uid and quantity
            #when quantity is change, it will update the session item quantity
            quantity_f = int(request.form['quantity'])
            itemuid_f = request.form['UID']

            for i in items:
                #find the item and update the quantity with the updated value
                if(itemuid_f ==  i['itemuid']):
                    if((quantity_f) == 0):
                        items.remove(i)
                    stocks = itemcontroller.get_item_by_UID(i['itemuid']).get_stocks()
                    if(quantity_f >  stocks):
                        flash("quantity exceeds stocks available.", "error")
                    else:
                        i['quantity'] = (quantity_f)
        for i in items:
            #this is the getting of the item object, and calculating total price for each item * quantity.
            cart_item = dict()
            cart_item['item'] = itemcontroller.get_item_by_UID(i['itemuid'])
            if(cart_item['item']):
                cart_item['quantity'] = i['quantity']
                cart_item['total'] = int(i['quantity']) * cart_item['item'].price_after_discount()
                cart_list.append(cart_item)
                subtotal_price = subtotal_price + cart_item['total']
                total_amount = subtotal_price

        if request.method == 'POST' and request.form.get('code'):
            #this part is when coupon code is inputted, it will check and update if it is valid by how much you save
            code = request.form.get('code')
            session['code'] = code
            coupon = itemcontroller.get_coupon_by_code(code)
            if coupon:
                if coupon.check_validity():
                    discount = coupon.get_discount(subtotal_price)
                    session['discount'] = discount
                else:
                    flash("Coupon code has expired, please try another code.", "nocoupon")
            else:
                flash("Coupon does not exists.", "nocoupon")
        if discount:
            total_amount = float(subtotal_price) - float(discount)
        session['total_amount'] = total_amount
        session['subtotal_price'] = subtotal_price
        return render_template('users/cart.html', cart_items=cart_list, subtotal_price=subtotal_price, discount=discount, code=code, total_amount=total_amount)
    else:
        return render_template('users/cart.html', cart_items=[],  subtotal_price=0.00, discount=discount, code=code, total_amount=total_amount)



@app.route('/cart/clear')
def del_cart():
    session.pop('cart', None)
    session.pop('discount', None)
    session.pop('subtotal_price', None)
    session.pop('total_amount', None)
    return redirect(url_for("cart"))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/checkout' , methods=['POST', 'GET'])
def checkout():
    user = session.get('logged_in_user')
    # if(not user):
    #     flash("Login or create an account first.", "error")
    #     return redirect(url_for('login'))
    form = checkout_form()
    items = session.get("cart")
    discount = session.get('discount')
    subtotal_price = session.get('subtotal_price')
    total_amount = session.get('total_amount')
    code = session.get('code')
    voucher = itemcontroller.get_coupon_by_UID(code)
    if(items):
        if form.validate_on_submit() and request.method == "POST":
            user = create_user_details(form.data, user)
            receipt = itemcontroller.checkout_items_users(items, voucher, user)
            return redirect(url_for("show_receipt", ruid=receipt.get_UID()))
    else:
        flash("You have nothing in your cart.", "error")
        return redirect(url_for("cart"))
    return render_template('users/checkout.html', form=form, subtotal_price=subtotal_price, total_amount=total_amount, discount=discount)


@app.route('/receipt/<ruid>', methods=['GET'])
def show_receipt(ruid):
    item = itemcontroller.get_receipt_by_UID(ruid)
    if not item:
        abort(404)
    return render_template("users/receipt.html", receipt=item)

@app.route('/allreceipt')
def show_all_receipt():
    username = session.get('logged_in_user')
    return render_template('about.html')


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










@app.route('/RetrieveAccount')
def retrieveAccount():
    accountDict = {}



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


# @app.route('/account/changepassword', methods = ['GET', 'POST'])
# def change_pass():
#     return render_template("base.html")


@app.route('/createFeedback', methods = ['GET', 'POST'])
def createFeedback():
    createFeedbackForm = CreateFeedbackForm(request.form)
    if request.method == 'POST' and createFeedbackForm.validate():
        usersDict = {}
        db = shelve.open('storage.db', 'c')

        try:
            usersDict = db['Feedback']
        except:
            print("Error in retrieving Users from storage.db.")

        feedback = Feedback.Feedback(createFeedbackForm.firstName.data, createFeedbackForm.email.data, createFeedbackForm.category.data, createFeedbackForm.feedback.data, createFeedbackForm.status.data, date= date.today())
        usersDict[feedback.get_userID()] = feedback
        db['Feedback'] = usersDict
        db.close()

        return redirect(url_for('retrieveFeedback'))
    return render_template('feedback/contact.html', form = createFeedbackForm)









if __name__ == '__main__':
 app.run(debug=True)
