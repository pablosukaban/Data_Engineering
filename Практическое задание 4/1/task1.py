import sqlite3
import pickle
import json


def write_to_file(filename, given_data):
    with open(filename, "w", encoding='utf-8') as r_json:
        r_json.write(
            json.dumps(
                given_data,
                indent=2,
                ensure_ascii=False,
            )
        )


with open('task_1_var_47_item.pkl', 'rb') as file:
    data = pickle.load(file)
    print(data)

conn = sqlite3.connect('data.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE "games" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "city" TEXT,
        "begin" TEXT,  
        "system" TEXT,  
        "tours_count" INTEGER,
        "min_rating" INTEGER, 
        "time_on_game" INTEGER
    );
'''

cursor.execute(create_table_query)

data_as_tuples = [(item["name"], item["city"], item["begin"], item["system"], item["tours_count"], item["min_rating"],
                   item["time_on_game"]) for item in data]

cursor.executemany('''
    INSERT INTO games ("name", "city", "begin", "system", "tours_count", "min_rating", "time_on_game")
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', data_as_tuples)

conn.commit()

# Запрос 1
var_value = 47
cursor.execute(f'SELECT * FROM games ORDER BY min_rating LIMIT ?', ((var_value + 10),))
result_1 = cursor.fetchall()

result_1 = [dict(row) for row in result_1]

write_to_file('output_1.json', result_1)

# Запрос 2
query = f'SELECT SUM(tours_count), MIN(tours_count), MAX(tours_count), AVG(tours_count) FROM games'
cursor.execute(query)
result_2 = cursor.fetchone()

result_2_dict = {
    'Sum': result_2[0],
    'Min': result_2[1],
    'Max': result_2[2],
    'Average': result_2[3]
}

write_to_file('output_2.json', result_2_dict)

# Запрос 3
cursor.execute(f'SELECT city, COUNT(*) as count FROM games GROUP BY city')
result_3 = cursor.fetchall()
result_3 = [dict(row) for row in result_3]

write_to_file('output_3.json', result_3)

# Запрос 4
var_predicate = 47
cursor.execute(f'SELECT * FROM games WHERE min_rating > 2000 ORDER BY time_on_game LIMIT ?',
               (var_predicate + 10,))
result_4 = cursor.fetchall()

result_4 = [dict(row) for row in result_4]

write_to_file('output_4.json', result_4)

conn.close()
