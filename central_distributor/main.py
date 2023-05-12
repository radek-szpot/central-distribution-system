from flask import Flask
from distributor.crud import ManufacturerCRUD
from distributor.database import create_database
import os

app = Flask(__name__)

URLS = ["ABC.COM", "DEF.COM"]


def add_manufacturers(urls):
    for url in urls:
        ManufacturerCRUD.create_manufacturer(url)


# Start the Flask application
if __name__ == "__main__":
    if not os.path.isfile('inventory.db'):
        create_database()
        add_manufacturers(URLS)
    app.run()
