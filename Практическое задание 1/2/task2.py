input_file = "text_1_var_47"

with open(input_file, 'r') as file:
    lines = file.readlines()

line_averages = [
    sum(map(int, line.strip().split(" "))) / len(line.strip().split(" "))
    for line in lines
]

output_filename = input_file + "_result"
with open(output_filename, "w") as file:
    file.write("\n".join(map(str, line_averages)))