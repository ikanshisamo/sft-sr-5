import re
import json
from pathlib import Path

def clean_latex(text):
    return re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', r'\1', text)

def clean_quotes(text):
    return re.sub(r"'([^']+)'", r'\1', text)

def process(data):
    for conv in data:
        for msg in conv.get("messages", []):
            role = msg.get("role")
            if role == "user":
                msg["content"] = clean_quotes(clean_latex(msg["content"]))
            elif role == "assistant":
                msg["content"] = clean_quotes(msg["content"])
    return data

BASE = Path(__file__).resolve().parents[1] / "all_output_generate"
RAW_DIR = BASE / "raw_data/final_essay_matematika.json"
CLEAN_DIR = BASE / "clean_data"
CLEAN_DIR.mkdir(exist_ok=True)

with open(RAW_DIR, "r", encoding="utf-8") as f:
    data = json.load(f)
output = process(data)
out_path = CLEAN_DIR / "final_essay_matematika_cleaned.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"Saved: {out_path}")