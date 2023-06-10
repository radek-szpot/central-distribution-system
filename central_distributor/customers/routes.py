import hashlib
from copy import deepcopy

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from markupsafe import Markup
from sqlalchemy.exc import IntegrityError, StatementError

from central_distributor.customers.crud import CustomerCRUD, PurchaseCRUD
from central_distributor.customers.serializers import product_serializer
from central_distributor.customers.validators import (
    is_customer_input_valid, items_still_available,
    redirect_unauthenticated_user)
from central_distributor.database import get_session
from central_distributor.distributor.crud import ManufacturerCRUD, ProductCRUD
from central_distributor.distributor.distributor import (
    send_manufacturer_sold_product, sum_quantities_of_duplicates)

customer_blueprint = Blueprint("customer_blueprint", __name__, template_folder='templates')
received_hashes = {}


@customer_blueprint.route('/')
def home():
    return render_template('index.html')


@customer_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        request_dict = request.form.to_dict()
        request_dict["pan_number"] = request_dict.get("pan_number") or None
        request_dict["cid_number"] = request_dict.get("cid_number") or None
        error_message = is_customer_input_valid(request_dict)
        if error_message:
            return render_template('signup.html', error_message=error_message)
        try:
            customer = CustomerCRUD.create(**request_dict)
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

        customer = CustomerCRUD.get_by_credentials(email, password)
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
        CustomerCRUD.update(session['customer_id'], **data)
        return redirect('/dashboard')
    return render_template('modify_account.html')


@customer_blueprint.route('/delete-account', methods=['POST'])
@redirect_unauthenticated_user
def delete_account():
    """Delete the customer's account details"""
    if request.method == 'POST':
        CustomerCRUD.delete(session['customer_id'])
        return redirect('/')
    return render_template('modify_account.html')


# Below endpoints with templates can be transferred to routes in distributor

@customer_blueprint.route('/dashboard')
@redirect_unauthenticated_user
def dashboard():
    """Display the customer's dashboard"""
    cart = session.get('cart', [])
    products = ProductCRUD.list()
    customer = CustomerCRUD.get(session.get('customer_id', []))
    return render_template('dashboard.html', cart=cart, products=products,
                           name=f"{customer.first_name} {customer.last_name}")


@customer_blueprint.route('/shopping-cart')
@redirect_unauthenticated_user
def shopping_cart(cc_missing=False, details_popup=""):
    """Display the customer's shopping-cart"""
    cart = session.get('cart', [])
    validated_cart = deepcopy(cart)
    whole_price = 0
    missing_items = []
    for item in cart:
        if not items_still_available(item["id"], item["user_quantity"]):
            missing_items.append(item)
            validated_cart.remove(item)
            continue
        price = item["user_quantity"] * item["singular_price"]
        item["price"] = price
        whole_price += price
    session['cart'] = validated_cart
    if not cc_missing and missing_items:
        missing_item_str = '<br>'.join([f'"{item["type"]}" from {item["manufacturer_name"]}' for item in missing_items])
        details_popup = Markup(
            f"Chosen items are not available anymore and thus were removed from cart:<br>{missing_item_str}"
        )

    return render_template('cart.html',
                           cart=validated_cart,
                           whole_price=whole_price,
                           cc_missing=cc_missing,
                           details_popup=details_popup,
                           conflict_popup=False, )


@customer_blueprint.route('/shopping-history')
@redirect_unauthenticated_user
def shopping_history():
    """Display the customer's shopping history"""
    purchases_history = PurchaseCRUD.get_by_customer(session.get('customer_id', []))
    return render_template('shopping_history.html', history=purchases_history)


@customer_blueprint.route('/add-to-cart/<int:product_id>', methods=['POST'])
@redirect_unauthenticated_user
def add_to_cart(product_id):
    user_quantity = int(request.form.get('user_quantity', 1))
    product = ProductCRUD.get(product_id)
    items_in_db = items_still_available(product_id, user_quantity, product)
    if not items_in_db:
        return shopping_cart(details_popup="Chosen items are not available anymore.")
    product.manufacturer_name = ManufacturerCRUD.get(product.manufacturer_id).name
    product_dict = product_serializer(product)
    product_dict['user_quantity'] = user_quantity

    # Get the current cart from the session
    cart = session.get('cart', [])
    cart.append(product_dict)
    cart = sum_quantities_of_duplicates(cart)
    session['cart'] = cart
    return redirect(url_for('customer_blueprint.dashboard'))


@customer_blueprint.route('/delete-from-cart/<int:product_id>', methods=['POST'])
@redirect_unauthenticated_user
def delete_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item["id"] != product_id]
    session['cart'] = cart
    return redirect(url_for('customer_blueprint.shopping_cart'))


@customer_blueprint.route('/buy', methods=['POST'])
@redirect_unauthenticated_user
def buy():
    cart = session.get('cart', [])
    customer_id = session.get('customer_id')
    customer = CustomerCRUD.get(customer_id)
    if not cart:
        return redirect('/dashboard')
    if not (customer.pan_number and customer.cid_number):
        return shopping_cart(cc_missing=True,
                             details_popup="Please complete your account details before making a purchase.")

    request_hash = hashlib.sha256(str(customer_id).encode()).hexdigest()

    if request_hash in received_hashes:
        return redirect('/shopping-cart')  # Redirect to avoid double submission

    received_hashes[request_hash] = True
    db_session = get_session()

    try:
        for item in cart:
            product = ProductCRUD.get(item["id"], db_session)
            if product and product.remaining_quantity >= item["user_quantity"]:
                purchase = PurchaseCRUD.get_all_fields(customer_id, item["id"], "Paid", db_session)
                if purchase:
                    PurchaseCRUD.update(purchase.id, item["user_quantity"], db_session)
                else:
                    PurchaseCRUD.create(customer_id, item["id"], item["user_quantity"], db_session)
                ProductCRUD.update_quantity(item["id"], item["user_quantity"], db_session)
                url = ManufacturerCRUD.get_by_name(item['manufacturer_name']).url
                send_manufacturer_sold_product(url)
            else:
                return shopping_cart()
        session['cart'] = []
        return redirect('/shopping-cart')
    finally:
        del received_hashes[request_hash]
