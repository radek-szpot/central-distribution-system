from central_distributor.distributor.crud import ProductCRUD, ManufacturerCRUD
import requests


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
    manufacturer_list = ManufacturerCRUD.get_manufacturer_list()
    products = fetch_products_information(manufacturer_list)

    for product_info in products:
        manufacturer_id = product_info.get("manufacturer_id")
        product_type = product_info.get("product_type")
        quantity = product_info.get("quantity")
        singular_price = product_info.get("singular_price")

        if product_type and quantity and singular_price is not None:
            ProductCRUD.create_or_update_product(manufacturer_id, product_type, quantity, singular_price)
        else:
            print("Invalid product information received")


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


def handle_customer_request(customer_request):
    # TODO: Handle customer requests and process the purchase
    # TODO: Update the database and notify manufacturers
    # TODO: Process the customer request
    # TODO: Update the database with the purchased goods
    # TODO: Notify manufacturers about the quantity of goods sold
    pass


def main():
    # FIXME: Below is shit from GPT
    # Main entry point of the distributor
    # Start listening for customer requests and handle them
    # Replace this with your actual implementation
    while True:
        customer_request = message_broker.receive_customer_request()
        handle_customer_request(customer_request)


"""
Description: This script represents the distributor module responsible for fetching goods information from each 
manufacturer's API. It uses the requests library to make HTTP GET requests to each manufacturer's /goods endpoint. 
The retrieved goods information is stored in a list for further processing.

In this example, the manufacturer_endpoints list contains the URLs of the manufacturers' APIs. 
You can add as many manufacturers as needed by including their respective endpoints.

The fetch_goods_information() function iterates over the manufacturer endpoints, retrieves the goods information 
from each manufacturer's API, and appends it to the goods_information list. 
You can further process or combine this information based on your specific requirements.

Remember to handle exceptions, error handling, and data processing according to your application's needs.

By following this approach, the distributor can communicate with each manufacturer's API separately, 
retrieve the goods information, and combine it as required. This allows the distributor to have a centralized 
view of the available goods from all manufacturers.
"""
