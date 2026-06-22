import json
import re

INPUT_FILE = r"D:\ara kuliah\semester 6\tim 5\sft_v4\data_proses_mat\proses_mat.json"

# kata-kata Inggris yang sering muncul
ENGLISH_WORDS = {
    "the", "is", "are", "was", "were", "have", "has", "had",
    "what", "why", "when", "where", "which", "who", "how",
    "and", "or", "but", "because", "with", "without",
    "student", "teacher", "learning", "answer", "question",
    "correct", "incorrect", "explain", "example", "information",
    "data", "system", "process", "result", "analysis"
}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

empty_count = 0
english_count = 0

for conv_idx, conv in enumerate(data):

    for msg_idx, msg in enumerate(conv.get("messages", [])):

        role = msg.get("role")

        if role not in {"user", "assistant"}:
            continue

        content = msg.get("content", "")

        # ======================
        # CEK KOSONG
        # ======================
        if not isinstance(content, str) or not content.strip():

            print("\n[KOSONG]")
            print(f"Conversation : {conv_idx}")
            print(f"Message      : {msg_idx}")
            print(f"Role         : {role}")

            print("\nISI CONVERSATION:")
            print(json.dumps(conv, ensure_ascii=False, indent=2))

        break

        # ======================
        # CEK BAHASA INGGRIS
        # ======================
        words = re.findall(r"\b[a-zA-Z]+\b", content.lower())

        if len(words) == 0:
            continue

        english_hits = sum(
            1 for w in words
            if w in ENGLISH_WORDS
        )

        ratio = english_hits / len(words)

        # jika >20% kata cocok dengan kamus Inggris
        if ratio > 0.20:

            english_count += 1

            preview = content[:300].replace("\n", " ")

            print("\n[INDIKASI INGGRIS]")
            print(f"Conversation : {conv_idx}")
            print(f"Message      : {msg_idx}")
            print(f"Role         : {role}")
            print(f"Ratio        : {ratio:.2%}")
            print(f"Preview      : {preview}")

print("\n" + "=" * 80)
print(f"Content kosong      : {empty_count}")
print(f"Indikasi Inggris    : {english_count}")