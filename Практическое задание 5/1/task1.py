import msgpack
from pymongo import MongoClient
from bson import json_util
import json


def write_to_file(filename, given_data):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(given_data, json_file, default=json_util.default, ensure_ascii=False)


client = MongoClient('localhost', 27017)

db = client['task5db']

with open('task_1_item.json', 'r') as file:
    data = json.load(file)

collection_name = 'task5collection'
collection = db[collection_name]

collection.delete_many({})

collection.insert_many(data)

result_1 = list(collection.find().sort("salary", -1).limit(10))
write_to_file('result_1.json', result_1)

result_2 = list(collection.find({"age": {"$lt": 30}}).sort("salary", -1).limit(15))
write_to_file('result_2.json', result_2)

result_3 = list(collection.find({
    "city": "Барселона",
    "job": {"$in": ["Инженер", "Врач", "Учитель"]}
}).sort("age", 1).limit(10))
write_to_file('result_3.json', result_3)

result_4_count = collection.count_documents({
    "age": {"$gte": 25, "$lte": 40},
    "year": {"$gte": 2019, "$lte": 2022},
    "$or": [
        {"salary": {"$gt": 50000, "$lte": 75000}},
        {"salary": {"$gt": 125000, "$lt": 150000}}
    ]
})
result_4 = {"count": result_4_count}
write_to_file('result_4.json', result_4)

client.close()
