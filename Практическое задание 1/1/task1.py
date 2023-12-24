import collections

file_name = "text_1_var_47"

with open(file_name) as f:
    lines = f.readlines()

word_counts = collections.Counter()

for line in lines:
    normal_line = (line.strip()
                   .replace("!", " ")
                   .replace("?", " ")
                   .replace(",", " ")
                   .replace(".", " ")
                   .strip())

    for word in normal_line.split():
        word_counts[word] += 1

sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

result_file_name = f"{file_name}_result"
with open(result_file_name, "w") as f:
    for word, count in sorted_word_counts.items():
        f.write(f"{word}:{count}\n")