from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from central_distributor.customers.crud import CustomerCRUD
from central_distributor.distributor.crud import ProductCRUD
from central_distributor.distributor.models import Product

customer_blueprint = Blueprint("customer_blueprint", __name__, template_folder='templates')


def product_serializer(obj):
    if isinstance(obj, Product):
        return {
            "id": obj.id,
            "manufacturer_id": obj.manufacturer_id,
            "type": obj.type,
            "quantity": obj.quantity,
            "singular_price": obj.singular_price,
        }
    raise TypeError("Object of type 'Product' is not JSON serializable")


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
def modify_account():
    """Modify the customer's account details"""
    # Retrieve the cart from the session
    if request.method == 'POST':
        # TODO
        return redirect('/dashboard')
    return render_template('modify_account.html')


# Below endpoints with templates can be transferred to routes in distributor

@customer_blueprint.route('/dashboard')
def dashboard():
    """Display the customer's dashboard"""
    is_user_logged_in = session.get('logged_in', False)
    if not is_user_logged_in:
        return redirect(url_for('customer_blueprint.login'))  # Redirect to the login page
    # Retrieve the cart from the session
    cart = session.get('cart', [])
    products = ProductCRUD.get_product_list()
    return render_template('dashboard.html', cart=cart, products=products)


@customer_blueprint.route('/shopping-cart')
def shopping_cart():
    """Display the customer's shopping-cart"""
    # Retrieve the cart from the session
    cart = session.get('cart', [])
    whole_price = 0
    for item in cart:
        price = item["user_quantity"] * item["singular_price"]
        item["price"] = price
        whole_price += price
    return render_template('cart.html', cart=cart, whole_price=whole_price)


@customer_blueprint.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = ProductCRUD.get_product(product_id)

    # Get the current cart from the session
    cart = session.get('cart', [])
    user_quantity = int(request.form.get('user_quantity', 1))

    # Add the product to the cart
    product_dict = product_serializer(product)
    product_dict['user_quantity'] = user_quantity
    cart.append(product_dict)

    # Update the cart in the session
    session['cart'] = cart
    flash(f"Added {user_quantity} {product.type}(s) to the cart", 'success')

    return redirect(url_for('customer_blueprint.dashboard'))


@customer_blueprint.route('/buy')
def buy():
    # TODO
    pass
