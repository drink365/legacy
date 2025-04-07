import streamlit as st
import json
import os

LANG_KEY = "app_language"

# 設定語言（使用者選擇後儲存在 session_state）
def set_language():
    lang = st.selectbox("🌐 請選擇語言 / Language / 语言", ["繁體中文", "English", "简体中文"])
    st.session_state[LANG_KEY] = {
        "繁體中文": "zh-TW",
        "English": "en",
        "简体中文": "zh-CN"
    }[lang]

# 根據語言代碼讀取對應語言的 JSON 文字檔
def get_text(key: str) -> str:
    lang_code = st.session_state.get(LANG_KEY, "zh-TW")  # 預設繁體中文
    file_path = f"lang/{lang_code}.json"
    
    # 如果檔案不存在，回傳 key 本身
    if not os.path.exists(file_path):
        return key

    # 讀取並回傳 key 對應的文字（找不到就顯示原始 key）
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(key, key)
    except Exception as e:
        return key
