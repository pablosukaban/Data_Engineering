import pickle
from pymongo import MongoClient
from bson import json_util
import json


def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, default=json_util.default, ensure_ascii=False)


client = MongoClient('localhost', 27017)

db = client['task5db']

file_path_task_2 = 'task_2_item.pkl'
with open(file_path_task_2, 'rb') as file_task_2:
    data_task_2 = pickle.load(file_task_2)

collection_name = 'task5collection'
collection = db[collection_name]

collection.insert_many(data_task_2)

result_salary_stats = collection.aggregate([
    {"$group": {
        "_id": "$job",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
write_to_file('result_salary_stats.json', list(result_salary_stats))

result_profession_count = collection.aggregate([
    {"$group": {
        "_id": "$job",
        "count": {"$sum": 1}
    }}
])
write_to_file('result_profession_count.json', list(result_profession_count))

result_salary_stats_by_city = collection.aggregate([
    {"$group": {
        "_id": "$city",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
write_to_file('result_salary_stats_by_city.json', list(result_salary_stats_by_city))

result_salary_stats_by_profession = collection.aggregate([
    {"$group": {
        "_id": "$job",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
write_to_file('result_salary_stats_by_profession.json', list(result_salary_stats_by_profession))

result_age_stats_by_city = collection.aggregate([
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
])
write_to_file('result_age_stats_by_city.json', list(result_age_stats_by_city))

result_age_stats_by_profession = collection.aggregate([
    {"$group": {
        "_id": "$job",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
])
write_to_file('result_age_stats_by_profession.json', list(result_age_stats_by_profession))

result_max_salary_at_min_age = list(collection.find().sort([("age", 1), ("salary", -1)]).limit(1))
write_to_file('result_max_salary_at_min_age.json', result_max_salary_at_min_age)

result_min_salary_at_max_age = list(collection.find().sort([("age", -1), ("salary", 1)]).limit(1))
write_to_file('result_min_salary_at_max_age.json', result_min_salary_at_max_age)

result_age_stats_by_city_with_salary_filter = collection.aggregate([
    {"$match": {"salary": {"$gt": 50000}}},
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }},
    {"$sort": {"_id": -1}}
])
write_to_file('result_age_stats_by_city_with_salary_filter.json', list(result_age_stats_by_city_with_salary_filter))

result_salary_stats_custom_filter = collection.aggregate([
    {"$match":
        {"$or": [
            {"age": {"$gt": 18, "$lt": 25}},
            {"age": {"$gt": 50, "$lt": 65}}
        ],
            "city": "Барселона",
            "job": {"$in": ["Учитель", "Строитель", "Программист"]}}
    },
    {"$group": {
        "_id": {"city": "$city", "job": "$job"},
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
])
write_to_file('result_salary_stats_custom_filter.json', list(result_salary_stats_custom_filter))

result_custom_aggregation = collection.aggregate([
    {"$match": {"job": {"$in": ["Учитель", "Строитель"]}}},
    {"$group": {
        "_id": "$city",
        "avg_salary": {"$avg": "$salary"}
    }},
    {"$sort": {"avg_salary": -1}}
])
write_to_file('result_custom_aggregation.json', list(result_custom_aggregation))

client.close()
