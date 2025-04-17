import os
import json

# Path to the 'Finished' folder with all disease subfolders and JSON files
root_dir = "mimic-iv-ext-direct-1.0.0/mimic-iv-ext-direct-1.0.0/Finished"

def extract_all_json_notes(root_dir):
    documents = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file_name in filenames:
            if file_name.endswith(".json"):
                full_path = os.path.join(dirpath, file_name)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        note = data.get("input2", "").strip()
                        if note:
                            documents.append({"id": file_name, "text": note})
                except Exception as e:
                    print(f"⚠️ Error reading {file_name}: {e}")
    if not documents:
        print("⚠️ Warning: No valid documents extracted. Check your dataset.")
    return documents

# Extract and save all notes
if __name__ == "__main__":
    docs = extract_all_json_notes(root_dir)
    with open("documents.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)
    print(f"✅ Saved {len(docs)} documents to documents.json")