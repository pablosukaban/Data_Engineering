import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
from zipfile import ZipFile


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


file_name = "[2]automotive.csv.zip"
column_types_name = "types.pkl"
ten_columns_name = "columns.csv"

column_info_dict = {}
unique_values_dict = {}
number_of_values = {}

chunk_generator = pd.read_csv(file_name, chunksize=1_000_000, compression="zip")

total_memory_usage = {}

objects = []

for i, chunk in enumerate(chunk_generator):
    for column in chunk.columns:
        if column not in column_info_dict:
            column_info_dict[column] = {
                "memory_usage": 0,
                "memory_percent": 0,
                "dtype": chunk[column].dtype,
            }

        column_info_dict[column]["memory_usage"] += (
                chunk[column].memory_usage(deep=True) // 1024
        )

        if chunk[column].dtype == "object":
            objects.append(column)
            if column not in unique_values_dict:
                unique_values_dict[column] = set()

            unique_values_dict[column].update(chunk[column].unique())
            number_of_values[column] = (
                    number_of_values.get(column, 0) + chunk[column].count()
            )

total_memory = sum(info["memory_usage"] for info in column_info_dict.values())
for column, info in column_info_dict.items():
    info["memory_percent"] = (info["memory_usage"] / total_memory) * 100

column_info_df = pd.DataFrame.from_dict(column_info_dict, orient="index")
file_size = {"file_size_KB": os.path.getsize(file_name) // 1024}
in_memory_size = {"file_in_memory_size_KB": total_memory}

write_stats_to_file(file_size, in_memory_size, column_info_df, "optimization.json")

chunk_generator = pd.read_csv(file_name, chunksize=1_000_000, compression="zip")

num_unique_values = {
    column: len(values) for column, values in unique_values_dict.items()
}

isFirst = True
types = {}

dfs = []
for i, chunk in enumerate(chunk_generator):
    for column in chunk.columns:
        if not isFirst:
            chunk[column] = chunk[column].astype(types[column])
        if column in objects:
            if num_unique_values[column] / number_of_values[column] < 0.5:
                chunk[column] = chunk[column].astype("category")
            else:
                chunk[column] = chunk[column].astype("object")
        elif isFirst and pd.api.types.is_integer_dtype(chunk[column]):
            chunk[column] = pd.to_numeric(chunk[column], downcast="unsigned")
        elif isFirst and pd.api.types.is_float_dtype(chunk[column]):
            chunk[column] = pd.to_numeric(chunk[column], downcast="float")
        else:
            continue
    if isFirst:
        types = chunk.dtypes.to_dict()
        isFirst = False
    dfs.append(chunk)

combined_df = pd.concat(dfs, ignore_index=True, sort=False)

combined_df.info(memory_usage="deep")
memory_stats = get_memory_stats(combined_df, file_name)
write_stats_to_file(
    memory_stats[0], memory_stats[1], memory_stats[2], "without_optimization.json"
)


def save_10_columns(my_df: pd.DataFrame):
    column_names = [
        "dealerID",
        "brandName",
        "modelName",
        "vf_AdaptiveCruiseControl",
        "isNew",
        "askPrice",
        "mileage",
        "vf_ABS",
        "vf_Doors",
        "interiorColor",
    ]
    types = my_df.dtypes.to_dict()
    first_chunk = True
    for chunk in pd.read_csv(
            file_name,
            usecols=lambda x: x in column_names,
            dtype=types,
            chunksize=1_000_000,
    ):
        chunk.to_csv(
            ten_columns_name,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )
        first_chunk = False

    compression_options = dict(method="zip", archive_name=column_types_name)
    pd.to_pickle(types, f"{column_types_name}.zip", compression=compression_options)


save_10_columns(combined_df)

with ZipFile(f"{ten_columns_name}.zip", "w") as myzip:
    myzip.write(ten_columns_name)

loaded_column_types = pd.read_pickle(f"{column_types_name}.zip", compression="zip")
df = pd.read_csv(
    f"{ten_columns_name}.zip", dtype=loaded_column_types, compression="zip"
)

# График 1: Количество автомобилей по брендам (Топ 10)
top_brands = df["brandName"].value_counts().nlargest(10).index

df_top_brands = df[df["brandName"].isin(top_brands)]

plt.figure(figsize=(12, 6))
sns.countplot(x="brandName", data=df_top_brands, order=top_brands)
plt.title("Количество автомобилей по брендам (Топ 10)")
plt.xlabel("Название бренда")
plt.ylabel("Количество")
plt.xticks(rotation=45, ha="right")
plt.savefig("plot1.png")
plt.close()

# График 2: Распределение новых и подержанных автомобилей
plt.figure(figsize=(10, 10))
df["isNew"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, explode=[0, 0.1])
plt.title("Распределение новых и подержанных автомобилей")
plt.ylabel("")
plt.savefig("plot2.png")
plt.close()

# Фильтрация данных по пробегу
df_filtered_msrp = df[(df["mileage"] >= 500) & (df["mileage"] <= 5000)]

# График 3: Ядерная оценка плотности для пробега от 500 до 5 000
plt.figure(figsize=(10, 6))
sns.kdeplot(df_filtered_msrp["mileage"], fill=True)
plt.title("Ядерная оценка плотности: Пробег от 500 до 5 000")
plt.xlabel("Пробег")
plt.ylabel("Плотность")
plt.savefig("plot3.png")
plt.close()

# График 4: Количество автомобилей по цветам салона (Топ 10)
top_colors = df["interiorColor"].value_counts().nlargest(10).index

df_top_colors = df[df["interiorColor"].isin(top_colors)]

plt.figure(figsize=(12, 6))
sns.countplot(x="interiorColor", data=df_top_colors, order=top_colors)
plt.title("Количество автомобилей по цветам салона (Топ 10)")
plt.xlabel("Цвет салона")
plt.ylabel("Количество")
plt.xticks(rotation=45, ha="right")
plt.savefig("plot4.png")
