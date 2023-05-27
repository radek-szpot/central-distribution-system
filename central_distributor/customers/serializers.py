from central_distributor.distributor.models import Product


def purchase_history_serializer(purchase):
    purchase_dict = {
        'id': purchase[0],
        'customer_id': purchase[1],
        'product_id': purchase[2],
        'quantity': purchase[3],
        'status': purchase[4],
        'product_type': purchase[5],
        'product_price': purchase[6],
        'manufacturer_name': purchase[7]
    }
    return purchase_dict


def product_serializer(obj):
    if isinstance(obj, Product):
        return {
            "id": obj.id,
            "manufacturer_name": obj.manufacturer_name if obj.manufacturer_name else obj.manufacturer_id,
            "type": obj.type,
            "quantity": obj.remaining_quantity,
            "singular_price": obj.singular_price,
        }
    raise TypeError("Object of type 'Product' is not JSON serializable")
