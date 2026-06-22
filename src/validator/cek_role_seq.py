import json

INPUT_FILE = r"D:\ara kuliah\semester 6\tim 5\sft_v4\ub-sr-05-sft-dataset-v1.jsonl"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

errors = []

user_user = 0
assistant_assistant = 0
system_system = 0
other_same = 0

# Kumpulkan semua error dulu
for conv_idx, conv in enumerate(data):

    messages = conv.get("messages", [])

    for i in range(len(messages) - 1):

        role1 = messages[i]["role"]
        role2 = messages[i + 1]["role"]

        if role1 == role2:

            errors.append((conv_idx, i))

            if role1 == "user":
                user_user += 1

            elif role1 == "assistant":
                assistant_assistant += 1

            elif role1 == "system":
                system_system += 1

            else:
                other_same += 1

print("=" * 100)
print("RINGKASAN")
print("=" * 100)
print(f"TOTAL SEQUENCE ERROR    : {len(errors)}")
print(f"user -> user           : {user_user}")
print(f"assistant -> assistant : {assistant_assistant}")
print(f"system -> system       : {system_system}")
print(f"lainnya                : {other_same}")
print("=" * 100)

# Tampilkan satu per satu
for no, (conv_idx, i) in enumerate(errors, start=1):

    messages = data[conv_idx]["messages"]

    print("\n" + "=" * 100)
    print(f"ERROR {no}/{len(errors)}")
    print(f"Conversation : {conv_idx}")
    print(f"Message {i} -> {i+1}")
    print(f"{messages[i]['role']} -> {messages[i+1]['role']}")

    print("\n--- MESSAGE 1 ---")
    print(messages[i]["content"][:1000])

    print("\n--- MESSAGE 2 ---")
    print(messages[i+1]["content"][:1000])

    input("\nENTER untuk lanjut...")