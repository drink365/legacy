import streamlit as st
import json
import os

# 語言資料夾路徑（已改為 i18n）
LANG_DIR = "i18n"

# 支援語言清單（可自行擴充）
LANGUAGES = {
    "zh-TW": "繁體中文",
    "en": "English",
    "zh-CN": "简体中文"
}

# 初始化語言
def set_language():
    if "language" not in st.session_state:
        st.session_state.language = "zh-TW"  # 預設語言

# 讀取語言對應文字
def get_text(key: str) -> str:
    lang = st.session_state.get("language", "zh-TW")
    lang_file = os.path.join(LANG_DIR, f"{lang}.json")

    try:
        with open(lang_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
        return translations.get(key, key)
    except Exception as e:
        return key  # 若找不到翻譯，就回傳原 key
