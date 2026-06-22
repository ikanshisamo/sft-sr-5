import json

INPUT_FILE = r"D:\ara kuliah\semester 6\tim 5\sft_v4\data_proses_mat\proses_mat.json"

VALID_ROLES = {"system", "user", "assistant"}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

error_count = 0

for conv_idx, conv in enumerate(data):

    messages = conv.get("messages", [])

    for msg_idx, msg in enumerate(messages):

        role = msg.get("role")

        if role not in VALID_ROLES:

            error_count += 1

            print("\n" + "=" * 80)
            print(f"Conversation : {conv_idx}")
            print(f"Message      : {msg_idx}")
            print(f"Role         : {role}")

print("\n" + "=" * 80)
print(f"TOTAL ROLE TIDAK VALID: {error_count}")