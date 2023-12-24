import csv

file_name = "text_4_var_47"
variant = 47
age = 25 + (variant % 10)
average_salary = 0
data = []

with open(file_name, newline="\n", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        item = {
            "number": int(row[0]),
            "name": f"{row[2]} {row[1]}",
            "age": int(row[3]),
            "salary": int(row[4][:-1])
        }

        average_salary += item["salary"]
        data.append(item)

average_salary /= len(data)

filtered_data = [item for item in data if item["salary"] > average_salary and item["age"] > age]

sorted_data = sorted(filtered_data, key=lambda item: item["number"])

for item in sorted_data:
    item["salary"] = f"{item['salary']}₽"

with open(file_name + "_result", 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in sorted_data:
        writer.writerow(item.values())