import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import json

file_name = "[5]asteroid.zip"
column_types_name = "column_types.pkl"
ten_columns_name = "10_columns.csv"

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

def insert_data(file_name, data_to_insert):
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data_to_insert, json_file, indent=2, ensure_ascii=False)

def get_memory_stats(df, file_name):
    file_size = {"file_size_KB": os.path.getsize(file_name) // 1024}

    memory_usage = df.memory_usage(deep=True)
    total_memory = memory_usage.sum()
    in_memory_size = {"file_in_memory_size_KB": total_memory // 1024}

    column_stat = pd.DataFrame(
        {
            "column_name": df.columns,
            "memory_abs": [memory_usage[key] // 1024 for key in df.columns],
            "memory_per": [
                round(memory_usage[key] / total_memory * 100, 4)
                for key in df.columns
            ],
            "dtype": df.dtypes.values,
        }
    )

    column_stat_sorted = column_stat.sort_values(by="memory_abs", ascending=False)
    return (file_size, in_memory_size, column_stat_sorted)

def change_obj_to_cat(df):
    for column in df.columns:
        if df[column].dtype == "object":
            unique_values = len(df[column].unique())
            total_values = len(df[column])
            if unique_values / total_values < 0.5:
                df[column] = df[column].astype("category")
        if pd.api.types.is_integer_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], downcast="unsigned")
        if pd.api.types.is_float_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], downcast="float")

def write_stats_to_file(file_stat, mem_stat, by_columns, output_file_name):
    with open(output_file_name, "w", encoding="utf-8") as r_json:
        combined_json = {}
        combined_json.update(file_stat)
        combined_json.update(mem_stat)
        res = by_columns.to_json(orient="index", default_handler=str)
        parsed = json.loads(res)
        combined_json.update(parsed)
        json.dump(combined_json, r_json, indent=2, ensure_ascii=False, cls=NpEncoder)

def change_types(my_df: pd.DataFrame):
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "without_optimization.json")
    print(my_df.info(memory_usage="deep"))
    change_obj_to_cat(my_df)
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "optimization.json")

def save_10_columns(my_df: pd.DataFrame):
    column_names = [
        "name",
        "neo",
        "H",
        "diameter",
        "epoch",
        "equinox",
        "ma",
        "sigma_e",
        "class",
        "rms",
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


my_df = pd.read_csv(file_name, compression="zip")
change_types(my_df)
save_10_columns(my_df)

loaded_column_types = pd.read_pickle(f"{column_types_name}.zip", compression="zip")
df = pd.read_csv(f"{ten_columns_name}.zip", dtype=loaded_column_types, compression="zip")

# Построение круговой диаграммы распределения топ-5 небесных тел по классу, за исключением MBA
plt.figure(figsize=(8, 8))
df['class'].value_counts().iloc[1:].nlargest(5).plot.pie(autopct='%1.1f%%', startangle=90)
plt.title('Распределение топ-5 небесных тел по классу, за исключением MBA')
plt.savefig('plot1.png')

# Построение круговой диаграммы распределения объектов, находящихся близко к Земле (Near-Earth Objects)
plt.figure(figsize=(8, 8))
df['neo'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
plt.title('Распределение объектов, находящихся близко к Земле (NEO)')
plt.savefig('plot2.png')

# Построение тепловой карты корреляции числовых столбцов
numeric_columns = df.select_dtypes(include=[float, int]).columns
correlation_matrix = df[numeric_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Тепловая карта корреляции')
plt.savefig('plot3.png')

# Построение точечного графика Mean Anomaly vs Eccentricity Sigma
plt.figure(figsize=(8, 6))
sns.scatterplot(x='ma', y='sigma_e', data=df)
plt.title('Точечный график Mean Anomaly vs Eccentricity Sigma')
plt.xlabel('Средняя аномалия (Mean Anomaly)')
plt.ylabel('Эксцентриситет Sigma (Eccentricity Sigma)')
plt.ylim(0, 5000)
plt.savefig('plot4.png')

# Построение диаграммы диаметра по классам небесных тел
plt.figure(figsize=(10, 6))
sns.boxplot(x='class', y='diameter', data=df)
plt.title('Диаграмма диаметра по классам небесных тел')
plt.xlabel('Класс')
plt.ylabel('Диаметр')
plt.ylim(0, 350)
plt.savefig('plot5.png')
