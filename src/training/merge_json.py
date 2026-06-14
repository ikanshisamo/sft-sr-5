from pathlib import Path
 
BASE = Path(__file__).resolve().parents[1] / "all_output_generate"
SEPARATE_DIR = BASE / "data_train" / "separate_data"
MERGE_DIR = BASE / "data_train" / "merge_data"
MERGE_DIR.mkdir(parents=True, exist_ok=True)
 
out_path = MERGE_DIR / "all_matematika_train.jsonl"
total = 0
 
with open(out_path, "w", encoding="utf-8") as out:
    for file in SEPARATE_DIR.glob("*.jsonl"):
        lines = file.read_text(encoding="utf-8").splitlines()
        for line in lines:
            out.write(line + "\n")
        total += len(lines)
        print(f"Merged: {file.name} ({len(lines)} lines)")
 
print(f"\nSaved: {out_path.name} ({total} total lines)")