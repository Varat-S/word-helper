import json
import re

def extract_latin_roots(word, filepath="data/English-word.jsonl"):
    latin_roots = set()
    word = word.lower()
    with open(filepath, 'r', encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("word", "").lower() == word:
                    templates = entry.get("etymology_templates", [])
                    for template in templates:
                        name = template.get("name")
                        args = template.get("args")
                        if name in ["bor", "der", "inh"] and args.get('2') == "la":
                            latin_roots.add(args.get('3'))
                    etymology_text = entry.get("etymology_text")
                    matches = re.findall(r"[Ff]rom Latin ([a-zA-Zōūīēáéóúāâêîôûàèìòùçñ\-]+)", etymology_text)
                    for match in matches:
                        latin_roots.add(match)
            except:
                continue
    return list(latin_roots)

print(extract_latin_roots("transport"))