from flask import Blueprint, render_template, request, redirect, session, url_for, flash, jsonify
from functools import wraps
from central_distributor.customers.crud import CustomerCRUD, PurchaseCRUD
from central_distributor.customers.serializers import product_serializer
from central_distributor.distributor.crud import ProductCRUD
from central_distributor.distributor.distributor import sum_quantities_of_duplicates
from central_distributor.database import get_session
import hashlib
from sqlalchemy.exc import IntegrityError, StatementError

customer_blueprint = Blueprint("customer_blueprint", __name__, template_folder='templates')
received_hashes = {}


def redirect_unauthenticated_user(endpoint):
    @wraps(endpoint)
    def decorated_function(*args, **kwargs):
        is_user_logged_in = session.get('logged_in', False)
        if not is_user_logged_in:
            return redirect(url_for('customer_blueprint.login'))
        return endpoint(*args, **kwargs)

    return decorated_function


def is_customer_input_valid(customer_dict):
    error_message = False
    if customer_dict["pan_number"] and len(customer_dict["pan_number"]) != 16:
        error_message = 'PAN number must be combination of 16 numbers!'
    if customer_dict["cid_number"] and len(customer_dict["cid_number"]) != 3:
        error_message = 'CID number must be combination of 3 numbers!'
    return error_message


@customer_blueprint.route('/')
def home():
    return render_template('index.html')


@customer_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        request_dict = request.form.to_dict()
        error_message = is_customer_input_valid(request_dict)
        if error_message:
            return render_template('signup.html', error_message=error_message)
        try:
            customer = CustomerCRUD.create_customer(**request_dict)
        except IntegrityError:
            error_message = 'Email is already in use!'
            return render_template('signup.html', error_message=error_message)
        except StatementError:
            error_message = 'PAN and CID numbers must be digits!'
            return render_template('signup.html', error_message=error_message)
        if customer:
            return render_template('login.html')
        return render_template('signup.html', error=True)

    return render_template('signup.html')


@customer_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        customer = CustomerCRUD.get_customer_by_credentials(email, password)
        if customer:
            session['logged_in'] = True
            session['customer_id'] = customer.id
            return redirect('/dashboard')

        # Invalid login, show error message
        return render_template('login.html', error=True)

    return render_template('login.html')


@customer_blueprint.route('/logout', methods=['POST'])
def logout():
    """Logout the user"""
    session.clear()
    return redirect(url_for('customer_blueprint.login'))


@customer_blueprint.route('/modify-account', methods=['GET', 'POST'])
@redirect_unauthenticated_user
def modify_account():
    """Modify the customer's account details"""
    if request.method == 'POST':
        data = {key: value for key, value in request.form.to_dict().items() if value.strip()}
        if not data:
            return render_template('modify_account.html')
        CustomerCRUD.update_customer(session['customer_id'], **data)
        return redirect('/dashboard')
    return render_template('modify_account.html')


@customer_blueprint.route('/delete-account', methods=['POST'])
@redirect_unauthenticated_user
def delete_account():
    """Delete the customer's account details"""
    if request.method == 'POST':
        CustomerCRUD.delete_customer(session['customer_id'])
        return redirect('/')
    return render_template('modify_account.html')


# Below endpoints with templates can be transferred to routes in distributor

@customer_blueprint.route('/dashboard')
@redirect_unauthenticated_user
def dashboard():
    """Display the customer's dashboard"""
    cart = session.get('cart', [])
    products = ProductCRUD.get_product_list()
    customer = CustomerCRUD.get_customer(session.get('customer_id', []))
    return render_template('dashboard.html', cart=cart, products=products,
                           name=f"{customer.first_name} {customer.last_name}")


@customer_blueprint.route('/get-remaining-quantities')
def get_remaining_quantities():
    products = ProductCRUD.get_product_list()
    remaining_quantities = {product.id: product.remaining_quantity for product in products}

    return jsonify(remaining_quantities=remaining_quantities)


@customer_blueprint.route('/shopping-cart')
@redirect_unauthenticated_user
def shopping_cart(details_popup=False, conflict_popup=False):
    """Display the customer's shopping-cart"""
    if conflict_popup:
        # todo: remove all items from group where there was a conflict and notify customer about that
        pass
    cart = session.get('cart', [])
    whole_price = 0
    for item in cart:
        price = item["user_quantity"] * item["singular_price"]
        item["price"] = price
        whole_price += price
    return render_template('cart.html', cart=cart, whole_price=whole_price, details_popup=details_popup,
                           conflict_popup=False)


@customer_blueprint.route('/shopping-history')
@redirect_unauthenticated_user
def shopping_history():
    """Display the customer's shopping history"""
    purchases_history = PurchaseCRUD.get_purchase_history(session.get('customer_id', []))
    print(purchases_history)
    return render_template('shopping_history.html', history=purchases_history)


@customer_blueprint.route('/add-to-cart/<int:product_id>', methods=['POST'])
@redirect_unauthenticated_user
def add_to_cart(product_id):
    user_quantity = int(request.form.get('user_quantity', 1))
    product = ProductCRUD.get_product(product_id)
    product_dict = product_serializer(product)
    product_dict['user_quantity'] = user_quantity

    # Get the current cart from the session
    cart = session.get('cart', [])
    cart.append(product_dict)
    cart = sum_quantities_of_duplicates(cart)

    # Update the cart in the session
    session['cart'] = cart
    flash(f"Added {user_quantity} {product.type}(s) to the cart", 'success')

    return redirect(url_for('customer_blueprint.dashboard'))


@customer_blueprint.route('/delete-from-cart/<int:product_id>', methods=['POST'])
@redirect_unauthenticated_user
def delete_from_cart(product_id):
    # Get the current cart from the session
    cart = session.get('cart', [])
    cart = [item for item in cart if item["id"] != product_id]
    # Update the cart in the session
    session['cart'] = cart
    return redirect(url_for('customer_blueprint.shopping_cart'))


@customer_blueprint.route('/buy')
@redirect_unauthenticated_user
def buy():
    cart = session.get('cart', [])
    customer_id = session.get('customer_id')
    customer = CustomerCRUD.get_customer(customer_id)
    if not cart:
        return redirect('/dashboard')
    if not (customer.pan_number and customer.cid_number):
        return shopping_cart(details_popup=True)

    request_hash = hashlib.sha256(str(customer_id).encode()).hexdigest()

    if request_hash in received_hashes:
        return redirect('/shopping-cart')  # Redirect to avoid double submission

    received_hashes[request_hash] = True
    db_session = get_session()

    try:
        for item in cart:
            product = ProductCRUD.get_product(item["id"], db_session)
            if product.remaining_quantity >= item["user_quantity"]:
                purchase = PurchaseCRUD.get_purchase_all_filters(customer_id, item["id"], db_session)
                if purchase:
                    PurchaseCRUD.update_purchase(purchase.id, item["user_quantity"], db_session)
                else:
                    PurchaseCRUD.create_purchase(customer_id, item["id"], item["user_quantity"], db_session)
                ProductCRUD.update_product_quantity(item["id"], item["user_quantity"], db_session)
            else:
                return shopping_cart(conflict_popup=True)
        session['cart'] = []
        return redirect('/shopping-cart')
    finally:
        del received_hashes[request_hash]
