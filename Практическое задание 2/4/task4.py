import json
import pickle


def update(given_product, given_price_info):
    methods = {
        "sum": lambda x, y: x + y,
        "sub": lambda x, y: x - y,
        "percent+": lambda x, y: x * (1 + y),
        "percent-": lambda x, y: x * (1 - y)
    }
    method = given_price_info["method"]
    param = given_price_info["param"]
    given_product["price"] = round(methods[method](given_product["price"], param), 2)


with open("products_47.pkl", "rb") as f:
    products = pickle.load(f)

with open("price_info_47.json") as f:
    price_info = json.load(f)

for price_item in price_info:
    for product in products:
        if product["name"] == price_item["name"]:
            update(product, price_item)
            break

with open("modified_data.pkl", "wb") as f:
    pickle.dump(products, f)
