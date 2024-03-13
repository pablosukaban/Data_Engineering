import xml.etree.ElementTree as ElemTree
import json
import os
from zipfile import ZipFile
from statistics import mean, stdev

all_data = []
label_frequency = {}

with ZipFile("zip_var_47.zip", "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()

        root = ElemTree.fromstring(html_content)

        name = root.find('name').text.strip()
        constellation = root.find('constellation').text.strip()
        spectral_class = root.find('spectral-class').text.strip()
        radius = int(root.find('radius').text.strip())
        rotation = float(root.find('rotation').text.split()[0])
        age = float(root.find('age').text.split()[0])
        distance = float(root.find('distance').text.split()[0])
        absolute_magnitude = float(root.find('absolute-magnitude').text.split()[0])

        data = {
            'name': name,
            'constellation': constellation,
            'spectral_class': spectral_class,
            'radius': radius,
            'rotation': rotation,
            'age': age,
            'distance': distance,
            'absolute_magnitude': absolute_magnitude
        }

        all_data.append(data)

        if constellation in label_frequency:
            label_frequency[constellation] += 1
        else:
            label_frequency[constellation] = 1

result_filepath = os.path.join('results', 'all_results.json')
os.makedirs('results', exist_ok=True)
with open(result_filepath, 'w', encoding='utf-8') as result_file:
    json.dump(all_data, result_file, ensure_ascii=False, indent=2)

sorted_data = sorted(all_data, key=lambda x: x['radius'])
sorted_filepath = os.path.join('results', 'sorted_results.json')

with open(sorted_filepath, 'w', encoding='utf-8') as sorted_file:
    json.dump(sorted_data, sorted_file, ensure_ascii=False, indent=2)

filtered_data = [item for item in all_data if item['spectral_class'] == 'T4B']
filtered_filepath = os.path.join('results', 'filtered_results.json')

with open(filtered_filepath, 'w', encoding='utf-8') as filtered_file:
    json.dump(filtered_data, filtered_file, ensure_ascii=False, indent=2)

distance_values = [item['distance'] for item in all_data]
distance_sum = sum(distance_values)
distance_min = min(distance_values)
distance_max = max(distance_values)
distance_avg = mean(distance_values)
distance_stdev = stdev(distance_values)

stats_data = {
    'distance_sum': distance_sum,
    'distance_min': distance_min,
    'distance_max': distance_max,
    'distance_avg': distance_avg,
    'distance_stdev': distance_stdev
}

stats_filepath = os.path.join('results', 'stats_results.json')

with open(stats_filepath, 'w', encoding='utf-8') as stats_file:
    json.dump(stats_data, stats_file, ensure_ascii=False, indent=2)

label_frequency_filepath = os.path.join('results', 'label_frequency.json')
with open(label_frequency_filepath, 'w', encoding='utf-8') as label_frequency_file:
    json.dump(label_frequency, label_frequency_file, ensure_ascii=False, indent=2)