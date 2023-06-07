from functools import wraps

from flask import redirect, session, url_for

from central_distributor.distributor.crud import ProductCRUD


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


def items_still_available(product_id, quantity, product=None):
    if not product:
        product = ProductCRUD.get(product_id)
    if product and product.remaining_quantity >= quantity:
        return True
    return False
