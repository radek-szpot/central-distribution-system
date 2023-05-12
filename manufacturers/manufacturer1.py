from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/goods", methods=["GET"])
def get_goods():
    # Retrieve goods information from the manufacturer's database or source
    goods_info = {
        "product_id": 1,
        "product_name": "Product A",
        "quantity": 100,
        # Add more details as needed
    }
    return jsonify(goods_info)


if __name__ == "__main__":
    app.run()
