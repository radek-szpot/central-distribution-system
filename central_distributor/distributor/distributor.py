import requests

from central_distributor.customers.crud import PurchaseCRUD
from central_distributor.distributor.crud import ManufacturerCRUD, ProductCRUD


def send_manufacturer_sold_product(manufacturer_url):
    response = requests.post(f"{manufacturer_url}/sold_product")
    if response.status_code != 200:
        print(f"Communication error with manufacturer {manufacturer_url}")


def fetch_products_information(manufacturer_list):
    products_information = []

    for manufacturer in manufacturer_list:
        endpoint = manufacturer.url
        try:
            response = requests.get(f"{endpoint}/all_products")
            if response.status_code == 200:
                products_info = response.json()
                products_info["manufacturer_id"] = manufacturer.id
                products_information.append(products_info)
            else:
                print(f"Error accessing goods information from {endpoint}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {endpoint}: {e}")

    return products_information


def update_available_products():
    manufacturer_list = ManufacturerCRUD.list()
    products = fetch_products_information(manufacturer_list)

    for product_info in products:
        manufacturer_id = product_info.get("manufacturer_id")
        product_type = product_info.get("product_type")
        quantity = product_info.get("quantity")
        singular_price = product_info.get("singular_price")

        if product_type and quantity and singular_price is not None:
            ProductCRUD.create_or_update(manufacturer_id, product_type, quantity, singular_price)
        else:
            print("Invalid product information received")


def update_products_status():
    purchases = PurchaseCRUD.list(["Paid"])
    for purchase in purchases:
        product = ProductCRUD.get(purchase.product_id)
        manufacturer = ManufacturerCRUD.get(product.manufacturer_id)
        send_manufacturer_sold_product(manufacturer.url)
        PurchaseCRUD.update(purchase.id, status="Passed to realisation")


def sum_quantities_of_duplicates(items):
    seen_ids = set()
    items_with_summed_quantity = []

    for item in items:
        if item['id'] in seen_ids:
            # If the id is already seen, find the corresponding item in the result list and update its quantity
            for existing_item in items_with_summed_quantity:
                if existing_item['id'] == item['id']:
                    existing_item['user_quantity'] += item['user_quantity']
                    break
        else:
            # If the id is not seen, add the item to the result list and mark the id as seen
            seen_ids.add(item['id'])
            items_with_summed_quantity.append(item)

    return items_with_summed_quantity
