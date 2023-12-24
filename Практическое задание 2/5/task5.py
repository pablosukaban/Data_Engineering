import json
import csv
import statistics
import msgpack
import pickle
import os

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def write_json_file(file_path, data):
    with open(file_path, 'w') as json_result_file:
        json.dump(data, json_result_file)

def write_csv_file(file_path, data, selected_fields):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(selected_fields)
        for item in data:
            writer.writerow([item[field] for field in selected_fields])

def write_msgpack_file(file_path, data):
    with open(file_path, 'wb') as msgpack_file:
        packed_data = msgpack.packb(data)
        msgpack_file.write(packed_data)

def write_pickle_file(file_path, data):
    with open(file_path, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

def get_file_size(file_path):
    return os.path.getsize(file_path)

def calculate_numeric_statistics(data, field):
    values = [item[field] for item in data]
    return {
        "Max": max(values),
        "Min": min(values),
        "Mean": statistics.mean(values),
        "Sum": sum(values),
        "StdDev": statistics.stdev(values)
    }

from collections import defaultdict

def calculate_string_frequency(values):
    frequency = defaultdict(int)
    for value in values:
        frequency[value] += 1
    return dict(frequency)


data = read_json_file('initial-data.json')

selected_fields = ['Price', 'QuantityInStock', 'WeightInGrams', 'LengthInCentimeters', 'WidthInCentimeters',
                   'UnitsSold']

results = {}

for field in selected_fields:
    values = [item[field] for item in data]

    if isinstance(values[0], (int, float)):
        results[field] = calculate_numeric_statistics(data, field)
    elif isinstance(values[0], str):
        results[field] = calculate_string_frequency(values)

write_json_file('results.json', results)
write_csv_file('data.csv', data, selected_fields)
write_msgpack_file('data.msgpack', data)
write_pickle_file('data.pkl', data)

json_size = get_file_size('results.json')
csv_size = get_file_size('data.csv')
msgpack_size = get_file_size('data.msgpack')
pkl_size = get_file_size('data.pkl')

with open('compare.txt', 'w') as compare_file:
    compare_file.write(f"Размер results.json: {json_size} байт\n")
    compare_file.write(f"Размер data.csv: {csv_size} байт\n")
    compare_file.write(f"Размер data.msgpack: {msgpack_size} байт\n")
    compare_file.write(f"Размер data.pkl: {pkl_size} байт\n")