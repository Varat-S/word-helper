import json

def extract_latin_roots(word, filepath="data/English-word.jsonl"):
    word = word.lower()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("word", "").lower() == word:
                    roots = []
                    for template in entry.get("etymology_templates", []):
                        args = template.get("args", {})
                        if args.get("2") == "la":  # Latin
                            roots.append(args.get("3"))  # The Latin root
                    return roots
            except json.JSONDecodeError:
                continue  # Skip lines that aren't valid JSON
    return []