import json

def find_words_with_latin_root(latin_root, filepath="data/English-word.jsonl"):
    latin_root = latin_root.lower()
    matches = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                for template in entry.get("etymology_templates", []):
                    args = template.get("args", {})
                    # Check all arg slots from 3 to 9 (sometimes Latin is stored in later args)
                    for key in ["3", "4", "5", "6", "7", "8", "9"]:
                        if args.get("2") == "la":
                            latin_candidate = args.get(key, "").lower()
                            if latin_root in latin_candidate:
                                matches.append(entry["word"])
            except json.JSONDecodeError:
                continue
    return list(set(matches))