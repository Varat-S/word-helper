import json

def find_words_with_latin_root(root_list, filepath="data/English-word.jsonl"):
    found_words = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                etym_templates = entry.get("etymology_templates", [])
                for template in etym_templates:
                    args = template.get("args", {})
                    if args.get("2") == "la":  # Latin
                        latin_root = args.get("3", "").lower()
                        if latin_root in root_list:
                            found_words.add(entry.get("word", "").lower())
            except:
                continue
    return sorted(found_words)