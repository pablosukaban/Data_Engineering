import json
import msgpack
import statistics
import os

with open('products_47.json', 'r') as json_file:
    product_data = json.load(json_file)

aggregated_data = {}

for item in product_data:
    name = item['name']
    price = item['price']

    if name not in aggregated_data:
        aggregated_data[name] = []

    aggregated_data[name].append(price)

for name, prices in aggregated_data.items():
    average_price = statistics.mean(prices)
    max_price = max(prices)
    min_price = min(prices)

    aggregated_data[name] = {
        "average_price": average_price,
        "max_price": max_price,
        "min_price": min_price
    }

with open('data.json', 'w') as json_output_file:
    json.dump(aggregated_data, json_output_file)

with open('data.msgpack', 'wb') as msgpack_output_file:
    packed_data = msgpack.packb(aggregated_data)
    msgpack_output_file.write(packed_data)

json_file_size = os.path.getsize('data.json')
msgpack_file_size = os.path.getsize('data.msgpack')

with open('compare.txt', 'w') as file:
    file.write(f"Размер 'data.json': {json_file_size} байт\n")
    file.write(f"Размер 'data.msgpack': {msgpack_file_size} байт\n")

with open('compare.txt', 'w') as file:
    file.write(f"Размер 'data.json': {json_file_size} байт\n")
    file.write(f"Размер 'data.msgpack': {msgpack_file_size} байт\n")

