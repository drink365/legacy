import json
import os
import streamlit as st

# 定義語系檔所在資料夾
LANG_DIR = "lang"

# 支援語言清單
AVAILABLE_LANGUAGES = {
    "zh_tw": "繁體中文",
    "en": "English",
    "zh_cn": "简体中文"
}

def load_language(lang_code):
    file_path = os.path.join(LANG_DIR, f"lang_{lang_code}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 設定語言（存在 session_state 中）
def set_language():
    if "language" not in st.session_state:
        st.session_state.language = "zh_tw"  # 預設語言：繁體中文
    selected_lang = st.sidebar.selectbox("🌐 語言 Language", options=list(AVAILABLE_LANGUAGES.keys()),
                                         format_func=lambda x: AVAILABLE_LANGUAGES[x])
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

# 根據目前語言載入對應翻譯檔
def get_text(key):
    lang_code = st.session_state.get("language", "zh_tw")
    lang_data = load_language(lang_code)
    return lang_data.get(key, key)
