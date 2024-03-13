import sqlite3
import os
import msgpack
import json
import pickle


def write_to_file(filename, data):
    with open(filename, "w", encoding='utf-8') as r_json:
        r_json.write(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )


if os.path.exists('data.db'):
    os.remove('data.db')

conn = sqlite3.connect('data.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE "songs" (
    "Id" INTEGER,
    "artist" TEXT,
    "song" TEXT,
    "duration_ms" INTEGER,
    "year" INTEGER,
    "tempo" REAL,
    "genre" TEXT,
    "acousticness" REAL, 
    "energy" REAL, 
    "popularity" INTEGER,
    "instrumentalness" REAL, 
    "explicit" BOOLEAN, 
    "loudness" REAL,
    PRIMARY KEY("Id" AUTOINCREMENT)
);
'''
cursor.execute(create_table_query)
conn.commit()

pkl_file_path = 'task_3_var_47_part_1.pkl'
# {'artist': 'Coldplay', 'song': 'Princess of China', 'duration_ms': '239215', 'year': '2011', 'tempo': '85.014',
# 'genre': 'rock, pop', 'acousticness': '0.00385', 'energy': '0.69', 'popularity': '66'}

data_to_insert = []

with open(pkl_file_path, 'rb') as pkl_file:
    data = pickle.load(pkl_file)

    for row in data:
        if all(value.strip() == '' or value == '0' for value in row):
            continue

        data_to_insert.append((
            row['artist'],  # artist
            row['song'],  # song
            int(row['duration_ms']),  # duration_ms
            int(row['year']),  # year
            float(row['tempo']),  # tempo
            row['genre'],  # genre
            row['acousticness'],  # acousticness
            row['energy'],  # energy
            row['popularity']  # popularity
        ))

if data_to_insert:
    cursor.executemany('''
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, acousticness, energy, popularity, instrumentalness, explicit, loudness)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, " ", " ", " ")
    ''', data_to_insert)

txt_file_path = 'task_3_var_47_part_2.text'
data_to_insert = []

with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    current_row = {}
    for line in txt_file:
        line = line.strip()
        if line == '=====':
            # добавляем текущую строку в список
            data_to_insert.append((
                current_row['artist'],
                current_row['song'],
                int(current_row['duration_ms']),
                int(current_row['year']),
                float(current_row['tempo']),
                current_row['genre'],
                float(current_row['instrumentalness']),
                current_row['explicit'] == 'True',
                float(current_row['loudness'])
            ))
            current_row = {}
        elif '::' in line:
            key, value = line.split('::')
            current_row[key] = value
    # добавляем последнюю строку в список
    if current_row:
        data_to_insert.append((
            current_row['artist'],
            current_row['song'],
            int(current_row['duration_ms']),
            int(current_row['year']),
            float(current_row['tempo']),
            current_row['genre'],
            float(current_row['instrumentalness']),
            current_row['explicit'] == 'True',
            float(current_row['loudness'])
        ))


# Insert data into table
cursor.executemany('''
    INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, acousticness, energy, popularity, instrumentalness, explicit, loudness)
    VALUES (?, ?, ?, ?, ?, ?, " ", " ", " ", ?, ?, ?)
''', data_to_insert)

conn.commit()

var = 47

# Запрос 1 вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;

select_query = '''
    SELECT * FROM songs
    ORDER BY duration_ms
    LIMIT ?
'''

cursor.execute(select_query, (var + 10,))
result_rows = cursor.fetchall()

result_rows = [dict(row) for row in result_rows]

write_to_file('output_data_1.json', result_rows)

# Запрос 2 вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
stats_query = '''
    SELECT
        SUM(duration_ms) as total_duration,
        MIN(duration_ms) as min_duration,
        MAX(duration_ms) as max_duration,
        AVG(duration_ms) as avg_duration
    FROM songs
'''

cursor.execute(stats_query)
stats_result = cursor.fetchone()

stats_data = {
    'Статистика по полю duration_ms': {
        'Total Duration': stats_result[0],
        'Min Duration': stats_result[1],
        'Max Duration': stats_result[2],
        'Average Duration': stats_result[3]
    }
}

write_to_file('output_data_2.json', stats_data)


# Запрос 3 вывод частоты встречаемости для категориального поля
frequency_query = '''
    SELECT year, COUNT(*) as frequency
    FROM songs
    GROUP BY year
    ORDER BY frequency DESC
'''

cursor.execute(frequency_query)
frequency_result = cursor.fetchall()

frequency_data = {'Частота по годам': {str(year): frequency for year, frequency in frequency_result}}
write_to_file('output_data_3.json', frequency_data)

# Запрос 4  вывод первых (VAR+15) отфильтрованных по произвольному
# предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.
filter_query = '''
    SELECT * FROM songs
    WHERE year > 2010
    ORDER BY duration_ms
    LIMIT ?
'''

cursor.execute(filter_query, (var + 15,))
filtered_result_rows = cursor.fetchall()

result_rows = [dict(row) for row in filtered_result_rows]

write_to_file('output_data_4.json', result_rows)

conn.close()
