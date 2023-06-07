import logging
import os
from datetime import datetime

from customers.crud import CustomerCRUD
from customers.routes import customer_blueprint
from distributor.crud import ManufacturerCRUD, ProductCRUD
from flask import Flask, request

from central_distributor.database import create_database
from central_distributor.simulation import run_scheduler

manufacturer_urls = [
    "http://127.0.0.1:5001/",
    "http://127.0.0.1:5002/",
    "http://127.0.0.1:5003/",
]

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(customer_blueprint)


def add_test_setup(urls):
    for i, url in enumerate(urls):
        ManufacturerCRUD.create(url, f"Manufacturer {chr(i + 65)}")
    if not ProductCRUD.list():
        ProductCRUD.create("1", "apple", 100, 3)
        ProductCRUD.create("1", "pear", 100, 5)
        ProductCRUD.create("2", "banana", 100, 7)
        ProductCRUD.create("3", "apple", 50, 4)
    if not CustomerCRUD.list():
        CustomerCRUD.create("abc@example.com", "a", "Radek", "Szpot")


@app.before_request
def log_request_info():
    remote_addr = request.environ.get("REMOTE_ADDR") or "-"
    method = request.method
    path = request.path
    http_version = request.environ.get("SERVER_PROTOCOL")
    timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    app.logger.info(f"{remote_addr} - - [{timestamp}] \"{method} {path} {http_version}\"")


def site_movement(manufacturer_interval, fake_client, app_, fake_simulation=False):
    run_scheduler(manufacturer_interval, fake_client, app_, fake_simulation)


if __name__ == "__main__":
    if not os.path.isfile('inventory.db'):
        create_database()
        add_test_setup(manufacturer_urls)
    client = app.test_client()
    site_movement(604800, client, app, fake_simulation=False)
    app.run(port=5000)
