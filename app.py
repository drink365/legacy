
import streamlit as st

st.set_page_config(page_title="永傳家族傳承教練", layout="centered")

st.image("logo.png", use_column_width=True)
st.title("歡迎來到永傳家族傳承教練")

col1, col2 = st.columns(2, gap="medium")
with col1:
    if st.button("我是顧問端使用者", use_container_width=True):
        st.switch_page("pages/advisor_home.py")
with col2:
    if st.button("我是客戶端使用者", use_container_width=True):
        st.switch_page("pages/client_home.py")
