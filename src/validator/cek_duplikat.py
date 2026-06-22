import json
from collections import Counter

INPUT_FILE = r"D:\ara kuliah\semester 6\tim 5\sft_v4\data_proses_mat\proses_mat.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

serialized = [
    json.dumps(x, ensure_ascii=False, sort_keys=True)
    for x in data
]

counter = Counter(serialized)

duplicates = 0

for text, freq in counter.items():

    if freq > 1:
        duplicates += freq - 1

print("TOTAL DUPLIKAT:", duplicates)