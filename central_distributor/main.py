from flask import Flask
from distributor.crud import ManufacturerCRUD, ProductCRUD
from central_distributor.database import create_database
from customers.routes import customer_blueprint
from customers.crud import CustomerCRUD, PurchaseCRUD
import os

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
        ManufacturerCRUD.create_manufacturer(url, f"Manufacturer {chr(i + 65)}")
    if not ProductCRUD.get_product_list():
        ProductCRUD.create_product("1", "apple", 100, 3)
        ProductCRUD.create_product("1", "pear", 100, 5)
        # ProductCRUD.create_product("2", "app", 50, 4)
        # ProductCRUD.create_product("2", "appa", 50, 4)
        # ProductCRUD.create_product("2", "appd", 51, 4)
        # ProductCRUD.create_product("2", "apps", 41, 4)
        # ProductCRUD.create_product("2", "appss", 56, 4)
        # ProductCRUD.create_product("2", "appssss", 21, 4)
        # ProductCRUD.create_product("2", "appsssss", 41, 4)
        # ProductCRUD.create_product("2", "ads", 1, 4)
        # ProductCRUD.create_product("2", "dsa", 2, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsa", 3, 4)
        # ProductCRUD.create_product("2", "dsadsa", 3, 4)
    if not CustomerCRUD.get_customer_list():
        CustomerCRUD.create_customer("radekulus@interia.pl", "a", "Radek", "Szpot")


if __name__ == "__main__":
    if not os.path.isfile('inventory.db'):
        create_database()
        add_test_setup(manufacturer_urls)
    print(f"manufacturers: {ManufacturerCRUD.get_manufacturer_list()}")
    print(f"products: {ProductCRUD.get_product_list()}")
    print(f"customers: {CustomerCRUD.get_customer_list()}")
    print(f"purchases: {PurchaseCRUD.get_purchases()}")
    app.run(port=5000)
