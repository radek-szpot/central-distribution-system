from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from functools import wraps
from central_distributor.customers.crud import CustomerCRUD, PurchaseCRUD
from central_distributor.distributor.crud import ProductCRUD
from central_distributor.distributor.models import Product
from central_distributor.distributor.distributor import sum_quantities_of_duplicates

customer_blueprint = Blueprint("customer_blueprint", __name__, template_folder='templates')


def product_serializer(obj):
    if isinstance(obj, Product):
        return {
            "id": obj.id,
            "manufacturer_id": obj.manufacturer_id,
            "type": obj.type,
            "quantity": obj.remaining_quantity,
            "singular_price": obj.singular_price,
        }
    raise TypeError("Object of type 'Product' is not JSON serializable")


def redirect_unauthenticated_user(endpoint):
    @wraps(endpoint)
    def decorated_function(*args, **kwargs):
        is_user_logged_in = session.get('logged_in', False)
        if not is_user_logged_in:
            return redirect(url_for('customer_blueprint.login'))
        return endpoint(*args, **kwargs)

    return decorated_function


@customer_blueprint.route('/')
def home():
    return render_template('index.html')


@customer_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        customer = CustomerCRUD.create_customer(**request.form.to_dict())
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


@customer_blueprint.route('/modify-account')
@redirect_unauthenticated_user
def modify_account():
    """Modify the customer's account details"""
    # Retrieve the cart from the session
    if request.method == 'POST':
        # TODO
        return redirect('/dashboard')
    return render_template('modify_account.html')


# Below endpoints with templates can be transferred to routes in distributor

@customer_blueprint.route('/dashboard')
@redirect_unauthenticated_user
def dashboard():
    """Display the customer's dashboard"""
    # Retrieve the cart from the session
    cart = session.get('cart', [])
    products = ProductCRUD.get_product_list()
    print(products)
    return render_template('dashboard.html', cart=cart, products=products)


@customer_blueprint.route('/shopping-cart')
@redirect_unauthenticated_user
def shopping_cart(show_popup=False):
    """Display the customer's shopping-cart"""
    # Retrieve the cart from the session
    cart = session.get('cart', [])
    whole_price = 0
    for item in cart:
        price = item["user_quantity"] * item["singular_price"]
        item["price"] = price
        whole_price += price
    return render_template('cart.html', cart=cart, whole_price=whole_price, show_popup=show_popup)


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
    if not (customer.pan_number or customer.cid_number):
        return shopping_cart(show_popup=True)
    if not cart:
        return redirect('/dashboard')

    for item in cart:
        PurchaseCRUD.create_purchase(customer_id, item["id"], item["user_quantity"])
        ProductCRUD.update_product_quantity(item["id"], item["user_quantity"])
    session['cart'] = []
    return redirect('/shopping-cart')
