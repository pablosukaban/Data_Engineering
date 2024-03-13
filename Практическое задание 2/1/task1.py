import numpy as np
import json

main_matrix = np.load('matrix_47.npy')

total_sum = np.sum(main_matrix)
total_avg = np.mean(main_matrix)

main_diagonal = np.diagonal(main_matrix)
sum_main_diagonal = np.sum(main_diagonal)
avg_main_diagonal = np.mean(main_diagonal)

side_diagonal = np.diagonal(np.flipud(main_matrix))
sum_side_diagonal = np.sum(side_diagonal)
avg_side_diagonal = np.mean(side_diagonal)

max_value = np.max(main_matrix)
min_value = np.min(main_matrix)

result = {
    "sum": int(total_sum),
    "avr": float(total_avg),
    "sumMD": int(sum_main_diagonal),
    "avrMD": float(avg_main_diagonal),
    "sumSD": int(sum_side_diagonal),
    "avrSD": float(avg_side_diagonal),
    "max": int(max_value),
    "min": int(min_value)
}

with open('result.json', 'w') as json_file:
    json.dump(result, json_file)

normalized_matrix = (main_matrix - min_value) / (max_value - min_value)
np.save('normalized_matrix.npy', normalized_matrix)
