from flask import url_for, redirect, render_template, Flask, request, flash, session,abort
from flask_uploads import UploadSet, IMAGES,configure_uploads
import shelve
import backend.Feedback as Feedback
from backend.admin_url import admin_pages
from backend.settings import *
# from login.forms import customer_registration
from login.forms import UserRegistration, UserLogin
from backend.user_details import *
from backend.forms import CreateFeedbackForm, UpdateFeedbackForm,checkout_form,service_order
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from login.admin_and_users import *
from backend.appointment import *


app = Flask(__name__, template_folder='../templates', static_url_path="/static")

app.register_blueprint(admin_pages) #split url to 2 files: admin_url and init

####################################################################################
#main items controller
####################################################################################



UPLOAD_FOLDER = '/uploads/'
app.config['UPLOADED_IMAGES_DEST'] = '/uploads/'
app.config['SECRET_KEY'] = 'THISISNOTASECRETKEY'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PRODUCT'] = UPLOAD_FOLDER, 'product/'

images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))


####################################################################################
# requires users to be logged in before they can access certain functions like
# viewing all receipts and checking out
def user_authorize(f):
    # f is function
    @wraps(f)
    # this wraps the function

    # The special syntax *args in function definitions in python is used
    # to pass a variable number of arguments to a function. It is used to
    # pass a non-keyworded, variable-length argument list.

    # What *args allows you to do is take in more arguments than the number
    # of formal arguments that you previously defined. With *args, any number of
    # extra arguments can be tacked on to your current formal parameters
    # (including zero extra arguments).

    # For example : we want to make a multiply function that takes any number
    # of arguments and able to multiply them all together. It can be done using
    # *args.

    # Using the *, the variable that we associate with the * becomes an iterable
    # meaning you can do things like iterate over it, run some higher order
    # functions such as map and filter, etc.
    def decorated_function(*args, **kws):
    # **kws == **kwargs

    # The special syntax **kwargs in function definitions in python is
    # used to pass a keyworded, variable-length argument list. We use the
    # name kwargs with the double star. The reason is because the double
    # star allows us to pass through keyword arguments (and any number of them).
        if(session.get('logged_in_user')):
            return f(*args, **kws)
        else:
            flash("You must login/register first.")
            return redirect(url_for("login"))
    return decorated_function
####################################################################################
####################################################################################

####################################################################################
@app.route('/')
def home():
    doctors = itemcontroller.get_doctors()
    return render_template('home.html', doctors=doctors)
####################################################################################
@app.route('/shop/item')
def shop():
    # in shop_items, the html will list the item if the available flag is true.
    #using the marco in _shophelper.html
    #shop_helper will check if there's any discount and display accordingly.
    sales_items = itemcontroller.get_all_sales_items()
    # itemcontroller controls all items (eg if you want to take out/put into db,
    # use item controller (with exceptions)
    return render_template('users/shop_items.html', items = sales_items)
####################################################################################
####################################################################################
@app.route('/shop/service')
def shop_services():
    sales_services = itemcontroller.get_all_sales_services()
    return render_template('users/shop_services.html', items = sales_services)
####################################################################################
# <serviceuid> will be taken from get_all_sales_services(serviceuid)
# eg: /shop/service/12345a
@app.route('/shop/service/<serviceuid>')
def shop_services_items(serviceuid):
    sales_service = itemcontroller.get_service_by_UID(serviceuid)
    form = service_order()
    return render_template('users/services.html', item = sales_service, form = form)
####################################################################################
@app.route('/shop/service/<serviceuid>/book', methods=['GET', 'POST'])
@user_authorize
def shop_services_book(serviceuid):
    user = session.get('logged_in_user')
    receipt = itemcontroller.get_receipt_by_user(user)
    # get code from session
    user_details = None
    if(receipt):
        user_details = receipt.get_user()
    # assign checkout form to form

    cart_list = []
    form = checkout_form()
    if(user_details):
        form.full_name.data = user_details.get_full_name()
        form.country.data = user_details.country
        form.street_addr.data = user_details.street_addr
        form.city.data = user_details.city
        form.postal.data = user_details.postal
        form.phone.data =  user_details.phone
        form.email.data =  user_details.email
        form.card_name.data =  user_details.card_name
    sales_service = itemcontroller.get_service_by_UID(serviceuid)
    total_price =  sales_service.price_after_discount()
    if(not sales_service):
        abort(404)
    date = request.args.get('date')
    time = request.args.get('time')
    if(not date or not time):
        abort(400)
    if request.method == "POST" and form.validate():
        user = session.get('logged_in_user')

        user_details = create_user_details(form.data, user)
        book_appointment = itemcontroller.create_appointment_and_save(date, time, user_details, sales_service.get_name())
        # create a receipt using item info (a list), coupon and user details
        receiptz = itemcontroller.checkout_services_users(sales_service,total_price, user_details)
        if( not book_appointment and not receiptz):
            abort(400)
        else:
            return redirect(url_for("shop_services_appointments"))

    return render_template('users/service_checkout.html', item = sales_service, form = form, total = total_price)
# ####################################################################################

@app.route('/shop/service/appointments')
def shop_services_appointments():
    itemcontroller.arrange_appointments()
    appointments = itemcontroller.get_all_appointments()
    return render_template('users/appointments.html', appointments=appointments)
# ####################################################################################
# ####################################################################################

@app.route('/doctors/<uid>')
def show_doctor(uid):
    doctorchosen = itemcontroller.get_doctor_by_uid(uid)
    return render_template('users/doctors.html', item=doctorchosen)
# ####################################################################################
# Unused at this point of time
@app.route('/shop/packages')
def shop_packages():
    sales_package = itemcontroller.get_all_sales_packages()
    return render_template('users/shop_packages.html', items = sales_package)

##########################################################################
@app.route('/contactus', methods=['GET', 'POST'])
def contact():
    createFeedbackForm = CreateFeedbackForm(request.form)
    if request.method == 'POST' and createFeedbackForm.validate():
        usersDict = {}
        db = shelve.open('feedstorage.db', 'c')

        try:
            usersDict = db['Feedback']

        except:
            print(Exception)
            print("Error in retrieving Users from feedstorage.db.")

        feedback = Feedback.Feedback(createFeedbackForm.firstName.data, createFeedbackForm.email.data, createFeedbackForm.category.data, createFeedbackForm.feedback.data, createFeedbackForm.status.data, date= date.today())
        usersDict[feedback.get_userID()] = feedback
        db['Feedback'] = usersDict

        db.close()
    return render_template('feedback/contact.html', form = createFeedbackForm)
####################################################################################
@app.route('/receipt.html')
def receipt():
    return render_template("users/receipt.html")
####################################################################################
@app.route('/shop/items/<itemuid>')
def shop_item(itemuid):
    item = itemcontroller.get_item_by_UID(itemuid)
    # if there is no item
    if(not item):
        abort(404)
    return render_template('users/item.html', item = item)
# item = item is to pass the object to the template so the template can be
# used to call methods

####################################################################################
@app.route('/cart/<itemuid>/add', methods=['POST'])
def add_item_to_cart(itemuid):
    num = 0
    item = itemcontroller.get_item_by_UID(itemuid)
    if(not item):
        abort(404)
    # if the session has no cart, set session cart to an empty list
    if not session.get('cart'):
        session['cart'] = []
    #     flag = False when item does not exist in cart
    flag = False
    for i in session['cart']:
        # session cannot store objects
        # so, loop through session cart to find if any item uid exists

        # check if item exists in the cart already
        if(itemuid == i['itemuid']):
            # get quantity from html form
            quantity = int(request.form['quantity'])
            # add quantity
            i['quantity'] += (quantity)
            # if quantity > stocks avail, flash message
            if(i['quantity'] > itemcontroller.get_item_by_UID(itemuid).get_stocks()):
                flash("Error, item quantity cannot exceed amount of stocks.", "error")
                return redirect(url_for("shop_item", itemuid=itemuid))
            else:
                flag = True
                flash("item already exists in cart, increase quantity by " + str(quantity), "success")
                break

    #if item is not in cart, add to cart
    if(not flag):
        appenditem = dict()
        appenditem['itemuid'] = itemuid
        # get quantity from html form
        quantity = int(request.form['quantity'])
        # if amount of items is less than or equal to total stocks, add and send
        # confirmation message via flash
        if(int(quantity) <= item.get_stocks()):
            appenditem['quantity'] = quantity
            session['cart'].append(appenditem)
            # success and error changes the colour of the flash message
            # success = green, error = red
            flash("Item added to cart.", "success")
        else:
            flash("Item not added to cart, quantity exceeds stocks available.", "error")
    return redirect(url_for("shop_item", itemuid=itemuid))
####################################################################################
@app.route('/cart/delete/<itemuid>')
def del_cart_item(itemuid):
    items = session.get("cart")
    # essentially allowing a new i to be added later
    remove = None
    for i in items:
        # find number of that item in cart and remove all quantities of that item
        if(itemuid ==  i['itemuid']):
            remove = i
    items.remove(remove)
    # update cart
    session['cart'] = items
    # show cart
    return redirect(url_for("cart"))
####################################################################################
@app.route('/cart', methods=['POST', 'GET'])
def cart():
    #need to input coupon code,removing of items and others
    items = session.get("cart")
    # all added items will be put into cart
    cart_list = []

    # there is no code unless there is an input in the field
    code = ''
    #clear the session code so that the data will not screw up.
    session['code'] = None
    # auto discount is 0.00
    discount = 0.00
    # every item add together - discount
    total_amount = 0
    if(items):
        # all items
        subtotal_price = 0
        if request.method == 'POST' and request.form.get('quantity'):
            # get value from the individual form of the uid and quantity
            # when quantity is change, it will update the session item quantity

            # quantity_f is the form quantity in cart
            quantity_f = int(request.form['quantity'])
            # itemuid_f is the form quantity in cart
            itemuid_f = request.form['UID']

            for i in items:
                # find the item and update the quantity with the updated value
                if(itemuid_f ==  i['itemuid']):
                    # if quantity is 0, remove from cart
                    if((quantity_f) == 0):
                        items.remove(i)
                        break
                    # if items =/= 0, get stocks from item controller. use itemuid to get stocks
                    stocks = itemcontroller.get_item_by_UID(i['itemuid']).get_stocks()
                    if(quantity_f >  stocks):
                        flash("Quantity exceeds stocks available.", "error")
                    else:
                        # add quantity into cart
                        i['quantity'] = (quantity_f)
        for i in items:
            # this is the getting of the item object, and calculating total price for each item * quantity
            # for displaying purposes

            # create a dictionary
            cart_item = dict()
            # get item object from itemcontroller in cart (based on itemuid)
            item = itemcontroller.get_item_by_UID(i['itemuid'])

            # if there exists the item in cart
            if (item):
                # cart_item = {"item":item_object}
                # item_object is sales_item
                cart_item['item'] = item

                stocks = item.get_stocks()
                # if stocks < quantity in cart
                if(stocks < i['quantity']):
                    # maxing out all stock amount
                    # if user request 10 and stocks only have 5, put 5
                    cart_item['quantity'] = stocks
                    flash("Quantity selected is more than stocks available.", "stockserror")
                else:
                    # add quantity to dictionary "cart_item"
                    cart_item['quantity'] = i['quantity']
                # total price = quantity * price
                cart_item['total'] = int(i['quantity']) * cart_item['item'].price_after_discount()
                # cart_item is for each item, cart_list is for full cart
                cart_list.append(cart_item)
                # add all totals of items to get final total
                # subtotal price is before  discount, total price is after discount.
                # if there is no discount, total amount = subtotal price
                subtotal_price = subtotal_price + cart_item['total']
                total_amount = subtotal_price
        if request.method == 'POST' and request.form.get('code'):
            # this part is when coupon code is inputted, it will check and update if it is valid by how much you save

            # get code from html form
            code = request.form.get('code')

            # retrieve coupon object from itemcontroller
            coupon = itemcontroller.get_coupon_by_code(code)
            # if coupon exists
            if coupon:
                # check if coupon is expired, whether it exists and if there is a minimum spending
                if coupon.check_validity():
                    # using coupon to get discount from subtotal price
                    discount = coupon.get_discount(subtotal_price)
                    # if coupon is valid but minimum spending is not met
                    if(discount == 0):
                        flash("Coupon requires a minimum spending of $" + "{0:.2f}".format(coupon.get_minimumspent()) , "nocoupon")
                    else:
                        # put code into session so I can access it easily later
                        session['code'] = code
                        # just to check code
                        print(session.get('code'))
                    # putting discount into session to be used in receipt and view all receipts
                    session['discount'] = discount
                # if coupon is expired
                else:
                    flash("Coupon code has expired, please try another code.", "nocoupon")
            # if coupon does not exist in database
            else:
                flash("Coupon does not exists.", "nocoupon")
        # if discount exists
        if discount:
            # get total amount by taking subtotal price - discount price to get the final price (total amount)
            total_amount = float(subtotal_price) - float(discount)
        # put total_amount and subtotal_price into session so I can access it easily later (for receipt and view all receipts)
        print(total_amount)
        session['total_amount'] = total_amount
        session['subtotal_price'] = subtotal_price

        # return the page cart and use cart_items=cart_list to fill up the fields (in the template)
        return render_template('users/cart.html', cart_items=cart_list, subtotal_price=subtotal_price, discount=discount, code=code, total_amount=total_amount)
    else:
        # if cart is empty
        return render_template('users/cart.html', cart_items=[],  subtotal_price=0.00, discount=discount, code=code, total_amount=total_amount)
####################################################################################
@app.route('/cart/clear')
def del_cart():
    # empty cart, it becomes none
    session.pop('cart', None)
    # empty discount, it becomes none
    session.pop('discount', None)
     # empty code, it becomes none
    session.pop('code', None)
    # empty subtotal price, it becomes none
    session.pop('subtotal_price', None)
    # empty total amount, it becomes none
    session.pop('total_amount', None)

    return redirect(url_for("cart"))
####################################################################################
@app.route('/about')
def about():
    return render_template('about.html')
####################################################################################
@app.route('/checkout' , methods=['POST', 'GET'])
# user needs to be logged in to access this page. if user is not logged in
# redirect then to login page for users to register/login
@user_authorize
def checkout():
    # get code from session

    code = session.get('code')
    # get username from session
    user = session.get('logged_in_user')
    # get cart from session
    items = session.get("cart")
    # get discount from session
    discount = session.get('discount')
    # get subtotal price from session
    subtotal_price = session.get('subtotal_price')
    # get total amount from session
    total_amount = session.get('total_amount')

    receipt = itemcontroller.get_receipt_by_user(user)
    # get code from session
    user_details = None
    if(receipt):
        user_details = receipt.get_user()
    # assign checkout form to form

    cart_list = []
    form = checkout_form()
    if(user_details):
        form.full_name.data = user_details.get_full_name()
        form.country.data = user_details.country
        form.street_addr.data = user_details.street_addr
        form.city.data = user_details.city
        form.postal.data = user_details.postal
        form.phone.data =  user_details.phone
        form.email.data =  user_details.email
        form.card_name.data =  user_details.card_name
    if not items:
        flash("cart is empty, unable to checkout.","error")
        return redirect(url_for("cart"))
    # get coupon code from itemcontroller
    coupon = itemcontroller.get_coupon_by_code(code)
    # print the coupon for checking purposes while running
    # print(coupon)

    # if items exist
    if(items):
        for i in items:
            item = itemcontroller.get_item_by_UID(i['itemuid'])

            # if there exists the item in cart
            if (item):
                one_item = dict()
                one_item['quantity'] = i['quantity']
                one_item['item'] = item
                one_item['total'] = int(i['quantity']) * item.price_after_discount()

                cart_list.append(one_item)
        # if form validation works
        if form.validate_on_submit() and request.method == "POST":
            # create user details using the data from the form and assign it to user_details
            user_details = create_user_details(form.data, user)
            # create a receipt using item info (a list), coupon and user details
            receiptz = itemcontroller.checkout_items_users(items, coupon, user_details)
            # empty cart, it becomes none
            session.pop('cart', None)
            # empty code, it becomes none
            session.pop('code', None)
            # empty discount, it becomes none
            session.pop('discount', None)
            # empty subtotal price, it becomes none
            session.pop('subtotal_price', None)
            # empty total amount, it becomes none
            session.pop('total_amount', None)

            # generate a receipt for the user
            # receiptz.get_UID() is found in sales receipt
            return redirect(url_for("show_receipt", ruid=receiptz.get_UID()))
    else:
        # if cart is empty, user cannot checkout
        # if they try to go straight into http://127.0.0.1:5000/checkout without adding anything into cart first
        flash("You have nothing in your cart.", "error")
        return redirect(url_for("cart"))
    print()
    # return the page cart and use subtotal_price=subtotal_price to fill up the fields (in the template)
    return render_template('users/checkout.html', form=form, subtotal_price=subtotal_price, total_amount=total_amount, discount=discount,
                           cart_items=cart_list)
####################################################################################
@app.route('/receipt/<ruid>', methods=['GET'])
def show_receipt(ruid):
    # after user checkout, get receipt using uid from itemcontroller
    item = itemcontroller.get_receipt_by_UID(ruid)
    # if item does not exist
    if not item:
        # display 404 page
        abort(404)
    return render_template("users/receipt.html", receipt=item)
####################################################################################
@app.route('/receipt/all')
# user has to be logged in to view all previous receipts
@user_authorize
def show_all_receipt():
    # getting the username from session
    username = session.get('logged_in_user')
    # get the user's past receipts
    all_receipt = itemcontroller.get_all_receipt_by_name(username)
    # for checking purposes
    print(all_receipt)
    return render_template('users/showallreceipt.html', receipts=all_receipt)
####################################################################################
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
####################################################################################
# @app.route('/login')
# def login():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return render_template('home.html')
####################################################################################
# @app.route('/login/validation', methods=['POST'])
# def do_user_login():
#     username = request.form['username']
#     password = request.form['password']
#     user = logincontroller.login_user(username, password)
#     if user:
#         session['logged_in'] = True
#         session['logged_in_user'] = username
#
#     return redirect(url_for("login"))
####################################################################################
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = customer_registration()
#     if(logincontroller.find_user_username(form.username.data)):
#         flash("Username exists, please  choose another.", "error")
#     if request.method == 'POST' and form.validate():
#
#         flag = logincontroller.create_user_account(form.username.data, form.password.data, form.email.data)
#         if(flag):
#             flash("You have registered, please login", "success")
#             return redirect(url_for('login'))
#         else:
#             flash("you have failed to register, something went wrong, try again", "error")
#
#     return render_template('register.html', form=form)
####################################################################################
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session['logged_in_user'] = ''
    return redirect(url_for('home'))
####################################################################################
# To add custom error 404 page
@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404

# To add custom error 403 page
@app.errorhandler(403)
def error_403(e):
    return render_template('error_pages/403.html'), 403

# To add custom error 410 page
@app.errorhandler(410)
def error_410(e):
    return render_template('error_pages/410.html'), 410

# To add custom error 500 page
@app.errorhandler(500)
def error_500(e):
    return render_template('error_pages/500.html'), 500
####################################################################################


####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################

@app.route('/login', methods=["GET", "POST"])
def login():
    user_login = UserLogin(request.form)

    if request.method == "POST" and user_login.validate():

        usersDict = {}
        db = shelve.open("users.db", "r")

        try:
            usersDict = db["Users"]
        except:
            print("Unable to access shelve")
            abort(302)

        username = user_login.username.data
        password = user_login.password.data


        for id in usersDict:
            user = usersDict.get(id)
            if user.get_username() == username:
                if user.check_password(password):
                    session['logged_in'] = True
                    session["logged_in_user"] = user.get_username()
                    return redirect(url_for("home"))
        flash("Invalid details")
    return render_template('login.html', form=user_login)

@app.route('/register', methods=['GET', 'POST'])
def register():
    userRegister = UserRegistration(request.form)
    if request.method == 'POST' and userRegister.validate():
        usersDict = {}
        db = shelve.open('users.db', 'c')
        try:
            usersDict = db['Users']
        except:
            print("Error in retrieving Users from users.db.")
        #retard dont even save the fucking firstname last name. add for fuck.
        user = User(userRegister.username.data, userRegister.email.data, userRegister.password.data)
        usersDict[user.get_userID()] = user
        db['Users'] = usersDict
        db.close()
        flash("You have successfully created your account, please login.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=userRegister)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
