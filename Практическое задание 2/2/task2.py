import os
import numpy as np

threshold = 547
matrix = np.load('matrix_47_2.npy')

filtered_indices = np.array([])
filtered_values = np.array([])
filtered_other_values = np.array([])

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i, j] > threshold:
            filtered_indices = np.append(filtered_indices, i)
            filtered_values = np.append(filtered_values, j)
            filtered_other_values = np.append(filtered_other_values, matrix[i, j])

result_file_path = 'result.npz'
result_compressed_path = 'result_compressed.npz'

np.savez(result_file_path, indices=filtered_indices, values=filtered_values, other_values=filtered_other_values)
np.savez_compressed(result_compressed_path, indices=filtered_indices, values=filtered_values, other_values=filtered_other_values)

result_file = np.load(result_file_path)
result_compressed = np.load(result_compressed_path)

file_size_result = os.path.getsize(result_file_path)
file_size_result_compressed = os.path.getsize(result_compressed_path)

with open('compare.txt', 'w') as file:
    file.write(f"Размер '{result_file_path}': {file_size_result} байт\n")
    file.write(f"Размер '{result_compressed_path}': {file_size_result_compressed} байт\n")