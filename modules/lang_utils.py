import streamlit as st
import json
import os

def set_language():
    lang = st.selectbox(
        "🌐 語言 / Language / 語言",
        options=["繁體中文", "English", "简体中文"],
        index=["繁體中文", "English", "简体中文"].index(get_lang_name(st.session_state.get("app_language", "zh-TW")))
    )
    lang_code = get_lang_code(lang)

    lang_changed = st.session_state.get("app_language") != lang_code
    st.session_state["app_language"] = lang_code

    lang_path = f"languages/{lang_code}.json"
    if os.path.exists(lang_path):
        with open(lang_path, "r", encoding="utf-8") as f:
            st.session_state["_translations"] = json.load(f)
    else:
        st.session_state["_translations"] = {}

    return lang_changed

def get_text(key):
    return st.session_state.get("_translations", {}).get(key, key)

def get_lang_name(code):
    return {
        "zh-TW": "繁體中文",
        "en": "English",
        "zh-CN": "简体中文"
    }.get(code, "繁體中文")

def get_lang_code(name):
    return {
        "繁體中文": "zh-TW",
        "English": "en",
        "简体中文": "zh-CN"
    }.get(name, "zh-TW")

get_text.__name__ = "_"
