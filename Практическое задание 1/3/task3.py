import math

file_name = "text_3_var_47"
threshold = 47

with open(file_name) as file:
    lines = file.readlines()

all_lines = []

for line in lines:
    nums = line.strip().split(",")
    new_nums = []
    for i in range(len(nums)):
        if nums[i] != "NA":
            new_nums.append(float(nums[i]))
        else:
            new_nums.append(float((int(nums[i - 1]) + int(nums[i + 1])) / 2))
    new_nums = [num for num in new_nums if math.sqrt(num) >= (threshold + 50)]
    all_lines.append(new_nums)

output_filename = f"{file_name}_result"

with open(output_filename, "w") as output_file:
    for row in all_lines:
        output_file.write(",".join(str(int(num)) for num in row))
        output_file.write("\n")