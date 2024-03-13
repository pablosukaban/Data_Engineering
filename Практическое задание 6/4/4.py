import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import json

file_name = "[4]vacancies.csv.gz"
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
    change_obj_to_cat(my_df)
    memory_stats = get_memory_stats(my_df, file_name)
    write_stats_to_file(memory_stats[0], memory_stats[1], memory_stats[2], "optimization.json")

def save_10_columns(my_df: pd.DataFrame):
    column_names = [
        "schedule_id",
        "accept_handicapped",
        "accept_kids",
        "experience_id",
        "employer_name",
        "salary_from",
        "salary_to",
        "area_name",
        "response_letter_required",
        "archived",
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


my_df = pd.read_csv(file_name, compression="gzip")
change_types(my_df)
save_10_columns(my_df)

loaded_column_types = pd.read_pickle(f"{column_types_name}.zip", compression="zip")
df = pd.read_csv(f"{ten_columns_name}.zip", dtype=loaded_column_types, compression="zip")


plt.figure(figsize=(10, 6))
sns.countplot(x='schedule_id', data=df)
plt.title('Количество работ для каждого расписания')
plt.savefig('plot1.png')

# Фильтрация данных по зарплате и создание графика KDE
df_filtered_salary = df[(df["salary_from"] >= 10000) & (df["salary_to"] <= 200000)]

plt.figure(figsize=(10, 6))
sns.kdeplot(df_filtered_salary["salary_from"], fill=True)
plt.title("Оценка плотности ядра зарплаты от 10,000 до 200,000")
plt.xlabel("Зарплата")
plt.ylabel("Плотность")
plt.savefig('plot2.png')

# Создание круговой диаграммы процента архивных вакансий
plt.figure(figsize=(8, 8))
df['archived'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, explode=[0, 0.1])
plt.title('Процент архивных вакансий')
plt.savefig('plot3.png')

# Выделение числовых столбцов и построение матрицы корреляции
numeric_columns = df.select_dtypes(include=[float, int]).columns
correlation_matrix = df[numeric_columns].corr()

# Построение тепловой карты корреляции
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Тепловая карта корреляции')
plt.savefig('plot4.png')

# Получение топ-5 районов с наибольшим количеством вакансий и построение графика
top_areas = df['area_name'].value_counts().nlargest(5)
plt.figure(figsize=(12, 6))
top_areas.plot(kind='bar', color='skyblue')
plt.title('Топ-5 районов с наибольшим числом вакансий')
plt.xlabel('Название района')
plt.ylabel('Количество вакансий')
plt.savefig('plot5.png')
