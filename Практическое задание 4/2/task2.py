import sqlite3
import msgpack
import json


def write_to_file(filename, data):
    with open(filename, "w", encoding='utf-8') as r_json:
        r_json.write(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )


with open('task_2_var_47_subitem.msgpack', 'rb') as file:
    data_2 = msgpack.unpackb(file.read())
    print(data_2)

conn = sqlite3.connect('data.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

create_table_query_2 = '''
    CREATE TABLE "games_competitions" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "place" INTEGER,
        "prise" INTEGER,
        FOREIGN KEY ("name") REFERENCES "books" ("name")
    );
'''
cursor.execute(create_table_query_2)

data_as_tuples = [(item["name"], item["place"], item["prise"]) for item in data_2]

cursor.executemany('''
        INSERT INTO games_competitions ("name", "place", "prise")
        VALUES (?, ?, ?)
    ''', data_as_tuples)

conn.commit()

# Запрос 1 первые 10 строк из таблицы games_competitions, где поле place больше 10
cursor.execute('''
    SELECT games_competitions.name, games_competitions.place, games_competitions.prise 
    FROM games
    JOIN games_competitions ON games.name = games_competitions.name
    WHERE games_competitions.place > 10
    LIMIT 10;
''')
result_1 = cursor.fetchall()
result_1 = [dict(row) for row in result_1]
write_to_file('output_1.json', result_1)

# Запрос 2 все игры, которые имеют более 10 туров и были проведены в городах, где также проводились соревнования,
# награда за которые превышает 500.
cursor.execute('''
    SELECT games.name
    FROM games
    JOIN games_competitions ON games.name = games_competitions.name
    WHERE games.min_rating > 2000 AND games_competitions.prise > 1000
    ORDER BY games.min_rating DESC;
''')
result_2 = cursor.fetchall()
result_2 = [dict(row) for row in result_2]
write_to_file('output_2.json', result_2)

# Запрос 3 все соревнования, которые проводились в городах, где было проведено более 5 игр.

cursor.execute('''
    SELECT games.city, AVG(games.time_on_game) as avg_time
    FROM games
    JOIN games_competitions ON games.name = games_competitions.name
    GROUP BY games.city
    HAVING COUNT(games_competitions.name) > 0
    ORDER BY avg_time DESC;
''')
result_3 = cursor.fetchall()
result_3 = [dict(row) for row in result_3]
write_to_file('output_3.json', result_3)

conn.close()
