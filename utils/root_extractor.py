import json
import re

def extract_latin_roots(word, filepath="data/English-word.jsonl", depth=1):
    word = word.lower()
    roots = set()

    def _load_entry(target):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("word", "").lower() == target:
                        return entry
                except json.JSONDecodeError:
                    continue
        return None

    def _extract(entry, current_depth):
        if not entry:
            return

        for template in entry.get("etymology_templates", []):
            args = template.get("args", {})

            # Case 1: explicit Latin root (e.g., "la:incorporeus")
            val = args.get("2", "")
            if val.startswith("la:"):
                roots.add(val[3:])

            # Case 2: implicit Latin root in other args (e.g., "la:corporeus" in args.get("1"))
            for arg in args.values():
                if isinstance(arg, str) and "la:" in arg:
                    match = re.search(r"la:([a-zA-Z-]+)", arg)
                    if match:
                        roots.add(match.group(1))

            # Case 3: root pointing to another English word (surface forms or suffixes)
            for key in ["2", "3", "1"]:
                val = args.get(key, "")
                if isinstance(val, str) and val.isalpha() and current_depth < depth:
                    nested = _load_entry(val)
                    _extract(nested, current_depth + 1)

    # Start
    main_entry = _load_entry(word)
    _extract(main_entry, 0)

    return list(roots)