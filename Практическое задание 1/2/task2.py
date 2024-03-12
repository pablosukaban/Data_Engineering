file_name = "text_1_var_47"

with open(file_name, 'r') as file:
    lines = file.readlines()

line_averages = [
    sum(map(int, line.strip().split(" "))) / len(line.strip().split(" "))
    for line in lines
]

result_file_name = file_name + "_result"
with open(result_file_name, "w") as file:
    file.write("\n".join(map(str, line_averages)))