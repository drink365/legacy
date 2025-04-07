# --- modules/lang_utils.py ---

import json
import os

LANG_FOLDER = "lang"

def load_language(lang_code="zh_tw"):
    file_path = os.path.join(LANG_FOLDER, f"lang_{lang_code}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Language file not found"}
