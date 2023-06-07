import json
import logging
import time
from random import choice, randint

from apscheduler.schedulers.background import BackgroundScheduler
from customers.crud import CustomerCRUD
from distributor.crud import ProductCRUD
from distributor.distributor import update_available_products
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def set_fake_customers(number_of_customers):
    customer_ids = []
    for i in range(number_of_customers):
        try:
            email = f"test_{i + 1}@example.com"
            password = f"test_{i + 1}"
            first_name = f"test_{i + 1}"
            last_name = f"test_{i + 1}"
            pan = "1" * 16
            cid = "1" * 3

            customer = CustomerCRUD.create(email, password, first_name, last_name, pan, cid)
            customer_ids.append((customer.id, email, password))
        except (SQLAlchemyError, IntegrityError) as e:
            customer_ids.append((i + 2, f"test_{i + 1}@example.com", f"test_{i + 1}"))
    return customer_ids


def login_and_get_session(client, email, password):
    login_response = client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)
    if login_response.status_code != 200:
        print(f"Failed to login for customer {email}. Status: {login_response.status_code}")
        return
    return login_response.headers.get('Set-Cookie')


def add_to_cart_and_get_session(client, session):
    product_ids = ProductCRUD.list_available_ids()
    if not product_ids:
        return
    product_id = choice(product_ids)
    items_quantity = randint(2, 5)
    data = {'user_quantity': str(items_quantity)}
    add_to_cart_response = client.post(f'http://localhost:5000/add-to-cart/{product_id}', data=json.dumps(data),
                                       headers={'Cookie': session}, follow_redirects=True)
    if add_to_cart_response.status_code != 200:
        print(f"Failed to add to cart {data}. Status: {add_to_cart_response.status_code}")
        return
    return add_to_cart_response.headers.get('Set-Cookie')


def buy_and_get_session(client, session):
    response = client.post(f'/buy', headers={'Cookie': session})
    if response.status_code == 200:
        print(f"Purchase successful")
    return response.headers.get('Set-Cookie')


def customer_buy_simulated_cart(client, email, password):
    session = login_and_get_session(client, email, password)
    time.sleep(2)
    session = add_to_cart_and_get_session(client, session)
    time.sleep(1)
    buy_and_get_session(client, session)


def run_scheduler(interval_in_seconds, client, app, simulation=False, number_of_fake_customers=2):
    customer_tuples = set_fake_customers(number_of_fake_customers)
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(update_available_products, 'interval', seconds=interval_in_seconds)
    if simulation:
        app.logger.setLevel(logging.INFO)

        for customer_tuple in customer_tuples:
            customer_id, email, password = customer_tuple
            scheduler.add_job(customer_buy_simulated_cart, 'interval', seconds=10,
                              args=[client, email, password])
            time.sleep(5)
        print("!! SIMULATION WILL START !!")
        print("Because of that many logs of fake customers will be displayed")
    scheduler.start()
