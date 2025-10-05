# app_config.py — central page config for Streamlit (applies to all pages)
import os
import streamlit as st

def ensure_page_config():
    # Set only once per app session
    if not st.session_state.get("_page_config_done", False):
        favicon_path = os.path.join(os.path.dirname(__file__), "favicon.png")
        try:
            st.set_page_config(
                page_title="影響力傳承策略平台",
                page_icon=favicon_path,
                layout="wide"
            )
        except Exception:
            # In case a subpage ran first and already set config, ignore
            pass
        st.session_state["_page_config_done"] = True
