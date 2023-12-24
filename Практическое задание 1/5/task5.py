from bs4 import BeautifulSoup
import csv

name = "text_5_var_47"

data = []

with open(name, encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")
    rows = soup.select("tr")[1:]

    for row in rows:
        cells = row.find_all("td")
        item = {
            "company": cells[0].text,
            "contact": cells[1].text,
            "country": cells[2].text,
            "price": cells[3].text,
            "item": cells[4].text,
        }
        data.append(item)

with open(name + "_result", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in data:
        writer.writerow(item.items())