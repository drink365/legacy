
if "page" not in st.session_state:
    st.session_state["page"] = None

if st.session_state["page"] == "client_home":
    import client_home
    st.stop()
elif st.session_state["page"] == "advisor_home":
    import advisor_home
    st.stop()


import streamlit as st
import base64

# 設定頁面
st.set_page_config(
    page_title="《影響力》 | 高資產家庭的傳承策略入口",
    page_icon="🌿",
    layout="centered"
)

# --- 導覽控制區 ---
if "page" not in st.session_state:
    st.session_state.page = None

if st.session_state.page == "client_home":
    import client_home
    st.stop()
elif st.session_state.page == "advisor_home":
    import advisor_home
    st.stop()

