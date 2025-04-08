import json
import os
import streamlit as st

LANG_DIR = "i18n"  # 確保你的語言檔都放在 i18n 資料夾下

def set_language(lang_code: str):
    """設定語言並載入對應語言檔"""
    if "language" not in st.session_state or st.session_state.language != lang_code:
        st.session_state.language = lang_code
    lang_file_path = os.path.join(LANG_DIR, f"{lang_code}.json")
    try:
        with open(lang_file_path, "r", encoding="utf-8") as f:
            st.session_state.translations = json.load(f)
    except FileNotFoundError:
        st.session_state.translations = {}

def get_text(key: str) -> str:
    """取得翻譯字串，若無對應則回傳 key 本身"""
    return st.session_state.get("translations", {}).get(key, key)
