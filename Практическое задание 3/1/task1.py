import json
import os
from bs4 import BeautifulSoup
from zipfile import ZipFile
from statistics import mean, stdev

all_data = []

with ZipFile("zip_var_47.zip", "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        city = soup.select_one('.build-wrapper > div:nth-child(1) > span').text.strip().replace('Город: ', '')
        structure_title = soup.select_one('.title').text.strip().replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('   ', ' ').replace('\r', '').replace('Строение: ', '')
        address = soup.select_one('.address-p').text.strip().replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('   ', ' ').replace('\r', '')
        floors = int(soup.select_one('.floors').text.split(':')[-1].strip())
        year_built = int(soup.select_one('.year').text.split()[-1].strip())
        parking = (soup.select('div:nth-child(3) > span')[2].text.strip().split(':')[-1].strip()) == "есть"
        image_url = soup.select_one('img')['src']
        rating = float(soup.select('div:nth-child(5) > span')[0].text.split(':')[-1].strip())
        views = int(soup.select('div:nth-child(5) > span')[1].text.split(':')[-1].strip())

        data = {
            'city': city,
            'structure_title': structure_title,
            'address': address,
            'floors': floors,
            'year_built': year_built,
            'parking': parking,
            'image_url': image_url,
            'rating': rating,
            'views': views
        }

        all_data.append(data)

result_filepath = os.path.join('results', 'all_results.json')
os.makedirs('results', exist_ok=True)

with open(result_filepath, 'w', encoding='utf-8') as result_file:
    json.dump(all_data, result_file, ensure_ascii=False, indent=2)

sorted_data = sorted(all_data, key=lambda x: x['rating'])
sorted_filepath = os.path.join('results', 'sorted_results.json')

with open(sorted_filepath, 'w', encoding='utf-8') as sorted_file:
    json.dump(sorted_data, sorted_file, ensure_ascii=False, indent=2)

filtered_data = [item for item in all_data if item['parking'] == True]
filtered_filepath = os.path.join('results', 'filtered_results.json')

with open(filtered_filepath, 'w', encoding='utf-8') as filtered_file:
    json.dump(filtered_data, filtered_file, ensure_ascii=False, indent=2)

views_values = [item['views'] for item in all_data]
views_sum = sum(views_values)
views_min = min(views_values)
views_max = max(views_values)
views_avg = mean(views_values)
views_stdev = stdev(views_values)

stats_data = {
    'views_sum': views_sum,
    'views_min': views_min,
    'views_max': views_max,
    'views_avg': views_avg,
    'views_stdev': views_stdev
}

stats_filepath = os.path.join('results', 'stats_results.json')

with open(stats_filepath, 'w', encoding='utf-8') as stats_file:
    json.dump(stats_data, stats_file, ensure_ascii=False, indent=2)