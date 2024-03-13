import xml.etree.ElementTree as ET
import json
from statistics import mean, stdev
import os
from zipfile import ZipFile

all_clothing_data = []
label_frequency = {}

with ZipFile("zip_var_47.zip", "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()

        root = ET.fromstring(html_content)

        clothing_data = []

        for clothing_elem in root.findall('.//clothing'):
            clothing_id = clothing_elem.findtext('id')
            name = clothing_elem.findtext('name')
            category = clothing_elem.findtext('category')
            size = clothing_elem.findtext('size')
            color = clothing_elem.findtext('color')
            material = clothing_elem.findtext('material')
            price_str = clothing_elem.findtext('price')
            rating_str = clothing_elem.findtext('rating')
            reviews_str = clothing_elem.findtext('reviews')
            sporty = clothing_elem.findtext('sporty')

            clothing_id = clothing_id.strip() if clothing_id is not None else None
            name = name.strip() if name is not None else None
            category = category.strip() if category is not None else None
            size = size.strip() if size is not None else None
            color = color.strip() if color is not None else None
            material = material.strip() if material is not None else None
            price = int(price_str) if price_str is not None else None
            rating = float(rating_str) if rating_str is not None else None
            reviews = int(reviews_str) if reviews_str is not None else None
            sporty = sporty.strip() if sporty is not None else None

            data = {
                'id': clothing_id,
                'name': name,
                'category': category,
                'size': size,
                'color': color,
                'material': material,
                'price': price,
                'rating': rating,
                'reviews': reviews,
                'sporty': sporty
            }

            clothing_data.append(data)

            if category in label_frequency:
                label_frequency[category] += 1
            else:
                label_frequency[category] = 1

        all_clothing_data.extend(clothing_data)

result_filepath = os.path.join('results', 'all_results.json')
os.makedirs('results', exist_ok=True)
with open(result_filepath, 'w', encoding='utf-8') as result_file:
    json.dump(all_clothing_data, result_file, ensure_ascii=False, indent=2)

sorted_data = sorted(all_clothing_data, key=lambda x: x.get('price', 0))
sorted_filepath = os.path.join('results', 'sorted_clothing_data.json')

with open(sorted_filepath, 'w', encoding='utf-8') as sorted_file:
    json.dump(sorted_data, sorted_file, ensure_ascii=False, indent=2)

filtered_data = [item for item in all_clothing_data if item.get('category') == 'Jacket']
filtered_filepath = os.path.join('results', 'filtered_clothing_data.json')

with open(filtered_filepath, 'w', encoding='utf-8') as filtered_file:
    json.dump(filtered_data, filtered_file, ensure_ascii=False, indent=2)

price_values = [item.get('price', 0) for item in all_clothing_data]
price_sum = sum(price_values)
price_min = min(price_values)
price_max = max(price_values)
price_avg = mean(price_values)
price_stdev = stdev(price_values)

stats_data = {
    'price_sum': price_sum,
    'price_min': price_min,
    'price_max': price_max,
    'price_avg': price_avg,
    'price_stdev': price_stdev
}

stats_filepath = os.path.join('results', 'stats_clothing_data.json')

with open(stats_filepath, 'w', encoding='utf-8') as stats_file:
    json.dump(stats_data, stats_file, ensure_ascii=False, indent=2)

label_frequency_filepath = os.path.join('results', 'label_frequency.json')
with open(label_frequency_filepath, 'w', encoding='utf-8') as label_frequency_file:
    json.dump(label_frequency, label_frequency_file, ensure_ascii=False, indent=2)
