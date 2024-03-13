import csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['task5db']

collection_name = 'task5collection'
collection = db[collection_name]

file_path_task_3 = 'task_3_item.csv'

with open(file_path_task_3, 'r', encoding='utf-8') as file_task_3:
    csv_reader = csv.DictReader(file_task_3, delimiter=';')
    data_task_3 = list(csv_reader)

for doc in data_task_3:
    doc['age'] = int(doc['age'])
    doc['year'] = int(doc['year'])
    doc['id'] = int(doc['id'])
    doc['salary'] = int(doc['salary'])

collection.insert_many(data_task_3)

# 1
collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})

# 2
collection.update_many({}, {"$inc": {"age": 1}})

# 3
selected_professions = ["Программист", "Врач", "Учитель"]
collection.update_many({"profession": {"$in": selected_professions}},
                       {"$mul": {"salary": 1.05}})

# 4
selected_cities = ["Загреб", "Санкт-Петербург", "Вроцлав"]
collection.update_many({"city": {"$in": selected_cities}},
                       {"$mul": {"salary": 1.07}})

# 5
complex_predicate_filter = {
    "city": "Махадаонда",
    "job": {"$in": ["Инженер", "Программист", "Психолог"]},
    "age": {"$gte": 30, "$lte": 50}
}
collection.update_many(complex_predicate_filter, {"$mul": {"salary": 1.10}})


# 6
random_predicate_filter = {"year": {"$lt": 2010}}
collection.delete_many(random_predicate_filter)

client.close()