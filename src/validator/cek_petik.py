import json
import re

INPUT_FILE = r"D:\ara kuliah\semester 6\tim 5\sft_v4\data_proses_mat\proses_mat.json"


def split_header(content):

    pattern = r'^(\[Emosi:.*?\]\n\[Konteks:.*?\]\n)(.*)$'

    match = re.match(pattern, content, flags=re.DOTALL)

    if match:
        return match.group(1), match.group(2)

    return None, content


total = 0

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for conv_idx, conv in enumerate(data):

    first_user_found = False

    for msg_idx, msg in enumerate(conv.get("messages", [])):

        role = msg.get("role")
        content = msg.get("content")

        if not isinstance(content, str):
            continue

        if role == "system":
            continue

        text_to_check = content

        if role == "user" and not first_user_found:

            _, body = split_header(content)

            text_to_check = body

            first_user_found = True

        if '"' in text_to_check or "'" in text_to_check:

            total += 1

            print("\n" + "=" * 100)
            print(f"Conversation : {conv_idx}")
            print(f"Message      : {msg_idx}")
            print(f"Role         : {role}")

            # tampilkan lokasi petik
            chars = []

            if '"' in text_to_check:
                chars.append('"')

            if "'" in text_to_check:
                chars.append("'")

            print("Petik ditemukan :", chars)

            preview = text_to_check[:500].replace("\n", "\\n")
            print("Preview :", preview)

print("\n" + "=" * 100)
print("TOTAL TEMUAN PETIK :", total)