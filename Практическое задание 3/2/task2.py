import json
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile
from statistics import mean, stdev
import re

all_product_data = []
label_frequency = {}

with ZipFile("zip_var_47.zip", "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        product_data = []

        for pad_elem in soup.select('.pad'):
            product_item = pad_elem.select_one('.product-item')
            if not product_item:
                continue

            product_id = product_item.select_one('.add-to-favorite')['data-id']
            link = product_item.select_one('a[href^="/product/"]')['href']
            image_src = product_item.select_one('img')['src']
            description = product_item.select_one('span').get_text(strip=True)
            price = product_item.select_one('price').get_text(strip=True)
            bonus = product_item.select_one('strong').get_text(strip=True)
            bonus = re.sub(r'\D', '', bonus)

            characteristics = {}
            for li_elem in product_item.select('ul li'):
                char_type = li_elem['type']
                char_value = li_elem.get_text(strip=True)
                characteristics[char_type] = char_value

            data = {
                'product_id': product_id,
                'link': link,
                'image_src': image_src,
                'description': description,
                'price': price,
                'bonus': bonus,
                'characteristics': characteristics
            }

            product_data.append(data)

            if bonus in label_frequency:
                label_frequency[bonus] += 1
            else:
                label_frequency[bonus] = 1

        all_product_data.extend(product_data)

result_filepath = os.path.join('results', 'all_results.json')
os.makedirs('results', exist_ok=True)
with open(result_filepath, 'w', encoding='utf-8') as result_file:
    json.dump(all_product_data, result_file, ensure_ascii=False, indent=2)

sorted_data = sorted(all_product_data, key=lambda x: x.get('product_id', '0'))

sorted_filepath = os.path.join('results', 'sorted_product_data.json')
with open(sorted_filepath, 'w', encoding='utf-8') as sorted_file:
    json.dump(sorted_data, sorted_file, ensure_ascii=False, indent=2)

filtered_data = [item for item in all_product_data if item.get('characteristics', {}).get('sim') == '4 SIM']
filtered_filepath = os.path.join('results', 'filtered_product_data.json')
with open(filtered_filepath, 'w', encoding='utf-8') as filtered_file:
    json.dump(filtered_data, filtered_file, ensure_ascii=False, indent=2)

price_values = [int(item.get('price', '0 ₽').replace('₽', '').replace(' ', '')) for item in all_product_data]
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

stats_filepath = os.path.join('results', 'stats_product_data.json')
with open(stats_filepath, 'w', encoding='utf-8') as stats_file:
    json.dump(stats_data, stats_file, ensure_ascii=False, indent=2)

label_frequency_filepath = os.path.join('results', 'label_frequency.json')
with open(label_frequency_filepath, 'w', encoding='utf-8') as label_frequency_file:
    json.dump(label_frequency, label_frequency_file, ensure_ascii=False, indent=2)