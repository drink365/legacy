# pages/_ping.py — 極簡健康檢查（用來判斷是不是該頁本身出問題）
# -*- coding: utf-8 -*-
import streamlit as st
st.set_page_config(page_title="Ping", layout="wide")
st.title("✅ App 正常運作")
st.write("如果你能看到這一頁，代表部署與路由是好的。")
