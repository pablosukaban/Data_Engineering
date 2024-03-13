import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import json


# fix int64 is not serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def insert_data(given_file_name, data_to_insert):
    with open(given_file_name, "w", encoding="utf-8") as json_file:
        json.dump(data_to_insert, json_file, indent=2, ensure_ascii=False)


def get_memory_stats(data, given_file_name):
    file_size = {"file_size_KB": os.path.getsize(given_file_name) // 1024}

    memory_usage = data.memory_usage(deep=True)
    total_memory = memory_usage.sum()
    in_memory_size = {"file_in_memory_size_KB": total_memory // 1024}

    column_stat = pd.DataFrame(
        {
            "column_name": data.columns,
            "memory_abs": [memory_usage[key] // 1024 for key in data.columns],
            "memory_per": [
                round(memory_usage[key] / total_memory * 100, 4)
                for key in data.columns
            ],
            "dtype": data.dtypes.values,
        }
    )

    column_stat_sorted = column_stat.sort_values(by="memory_abs", ascending=False)
    return file_size, in_memory_size, column_stat_sorted


def change_obj_to_cat(data):
    for column in data.columns:
        if data[column].dtype == "object":
            unique_values = len(data[column].unique())
            total_values = len(data[column])
            if unique_values / total_values < 0.5:
                data[column] = data[column].astype("category")
        if pd.api.types.is_integer_dtype(data[column]):
            data[column] = pd.to_numeric(data[column], downcast="unsigned")
        if pd.api.types.is_float_dtype(data[column]):
            data[column] = pd.to_numeric(data[column], downcast="float")


def write_stats_to_file(file_stat, mem_stat, by_columns, output_file_name):
    with open(output_file_name, "w", encoding="utf-8") as r_json:
        combined_json = {}
        combined_json.update(file_stat)
        combined_json.update(mem_stat)
        res = by_columns.to_json(orient="index", default_handler=str)
        parsed = json.loads(res)
        combined_json.update(parsed)
        json.dump(combined_json, r_json, indent=2, ensure_ascii=False, cls=NpEncoder)


file_name = "[3]flights.csv"
column_types_name = "column_types.pkl"
ten_columns_name = "10_columns.csv"


def change_types(my_df: pd.DataFrame):
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "without_optimization.json")
    change_obj_to_cat(my_df)
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "optimization.json")


def save_10_columns(my_df: pd.DataFrame):
    column_names = [
        "YEAR",
        "MONTH",
        "DAY",
        "AIRLINE",
        "FLIGHT_NUMBER",
        "ORIGIN_AIRPORT",
        "DESTINATION_AIRPORT",
        "DEPARTURE_DELAY",
        "DISTANCE",
        "CANCELLED",
    ]
    types = my_df.dtypes.to_dict()
    rf = pd.read_csv(
        file_name,
        usecols=lambda x: x in column_names,
        dtype=types,
    )
    compression_options = dict(method="zip", archive_name=ten_columns_name)
    rf.to_csv(f"{ten_columns_name}.zip", index=False, compression="zip")

    compression_options = dict(method="zip", archive_name=column_types_name)
    pd.to_pickle(types, f"{column_types_name}.zip", compression=compression_options)


my_df = pd.read_csv(file_name)
change_types(my_df)
save_10_columns(my_df)

# Загрузка типов колонок
loaded_column_types = pd.read_pickle(f"{column_types_name}.zip", compression="zip")

# Загрузка данных
df = pd.read_csv(f"{ten_columns_name}.zip", dtype=loaded_column_types, compression="zip")

# График 1: Среднее время задержки по месяцам
average_delay_by_airline = df.groupby('MONTH')['DEPARTURE_DELAY'].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(average_delay_by_airline['MONTH'], average_delay_by_airline['DEPARTURE_DELAY'], color='skyblue')
plt.title('Среднее время задержки вылета по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Среднее время задержки вылета (минуты)')
plt.savefig('plot1.png')  # Сохранение в файл

# График 2: Общее количество рейсов по авиакомпаниям
plt.figure(figsize=(12, 6))
sns.countplot(x='AIRLINE', data=df)
plt.title('Общее количество рейсов по авиакомпаниям')
plt.xlabel('Авиакомпания')
plt.ylabel('Количество рейсов')
plt.savefig('plot2.png')  # Сохранение в файл

# График 3: Расстояние vs. Задержка вылета
plt.figure(figsize=(10, 6))
plt.scatter(df['DISTANCE'], df['DEPARTURE_DELAY'], alpha=0.5)
plt.title('Расстояние vs. Задержка вылета')
plt.xlabel('Расстояние')
plt.ylabel('Задержка вылета (минуты)')
plt.savefig('plot3.png')  # Сохранение в файл

# График 4: Процент отмененных рейсов
cancelled_counts = df['CANCELLED'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(cancelled_counts, labels=cancelled_counts.index, autopct='%1.1f%%', startangle=90,
        colors=['lightcoral', 'lightgreen'])
plt.title('Процент отмененных рейсов')
plt.savefig('plot4.png')  # Сохранение в файл

# График 5: Среднее время задержки по авиакомпаниям
average_delay_by_airline = df.groupby('AIRLINE')['DEPARTURE_DELAY'].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(average_delay_by_airline['AIRLINE'], average_delay_by_airline['DEPARTURE_DELAY'], color='skyblue')
plt.title('Среднее время задержки вылета по авиакомпаниям')
plt.xlabel('Авиакомпания')
plt.ylabel('Среднее время задержки вылета (минуты)')
plt.savefig('plot5.png')  # Сохранение в файл
