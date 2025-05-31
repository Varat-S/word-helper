import json

def get_etymology(word, filepath="data/English-word.jsonl"):
    word = word.lower()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("word", "").lower() == word:
                    return entry.get("etymology_text", "No etymology found.")
            except json.JSONDecodeError:
                continue
    return "No etymology found."