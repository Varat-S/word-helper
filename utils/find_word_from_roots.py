import json
import unicodedata
import re

def normalize_latin(s):
    """Normalize Latin text by removing diacritics and lowercasing."""
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.lower()

def find_words_with_latin_root(root_list, filepath="data/English-word.jsonl"):
    """Reverse search English words that share a Latin root — exact matches only."""
    found_words = set()
    root_list_norm = [normalize_latin(root) for root in root_list]

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            word = entry.get("word", "").lower()
            etym_templates = entry.get("etymology_templates", [])
            etymology_text = entry.get("etymology_text", "")

            # --- Check etymology_templates ---
            matched = False
            for template in etym_templates:
                name = template.get("name")
                args = template.get("args", {})
                if name in ["bor", "der", "inh"] and args.get("2") == "la":
                    latin_root = args.get("3", "")
                    latin_root_norm = normalize_latin(latin_root)
                    for root_norm in root_list_norm:
                        if root_norm == latin_root_norm:
                            found_words.add(word)
                            matched = True
                            break
                if matched:
                    break  # Skip further templates if already matched

            if matched:
                continue  # Skip text check if already matched

            # --- Check etymology_text ---
            matches = re.findall(r"[Ff]rom Latin ([a-zA-Zōūīēáéóúāâêîôûàèìòùçñ\-]+)", etymology_text)
            for match in matches:
                match_norm = normalize_latin(match)
                for root_norm in root_list_norm:
                    if root_norm == match_norm:
                        found_words.add(word)  # Original English word, unmodified
                        break

    return sorted(found_words)