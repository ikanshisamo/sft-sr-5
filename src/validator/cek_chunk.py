import json
import re

INPUT_FILE = r"D:\ara kuliah\semester 6\tim 5\sft_v4\data_proses_bindo\proses_bindo_2.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0

for conv_idx, conv in enumerate(data):

    for msg_idx, msg in enumerate(conv.get("messages", [])):

        content = str(msg.get("content", ""))

        if re.search(r'\[Konteks:\s*[^"\]]+\.json\]', content):

            count += 1

            print("\n" + "=" * 100)
            print(f"TEMUAN {count}")
            print(f"Conversation : {conv_idx}")
            print(f"Message      : {msg_idx}")
            print(f"Role         : {msg.get('role')}")

            match = re.search(
                r'\[Konteks:\s*[^"\]]+\.json\]',
                content
            )

            print("Konteks      :", match.group(0))

print("\n" + "=" * 100)
print("Konteks tanpa petik:", count)