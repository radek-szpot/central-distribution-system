from flask import Flask, jsonify
from helpers import generate_random_number, generate_random_fruit

app = Flask(__name__)


@app.route("/all_products", methods=["GET"])
def get_all_products():
    goods_info = {
        "product_type": generate_random_fruit(),
        "quantity": generate_random_number(),
        "singular_price": generate_random_number(2, 5),
    }
    return jsonify(goods_info)


if __name__ == "__main__":
    app.run(port=5001)
