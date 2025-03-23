import streamlit as st

# --- 網頁基本設定 ---
st.set_page_config(
    page_title="永傳 AI 教練",
    page_icon="🌿",
    layout="centered"
)

# --- 品牌標題區 ---
st.markdown("### 永傳")
st.markdown("#### 傳承您的影響力")

st.markdown("---")

# --- 模組一 開場語 (K版) ---
st.markdown("## 模組一：經營的是事業，留下的是故事")

st.markdown("""
我們陪您一起梳理這段歷程，  
為後人留下的不只是成果，更是一種精神。
""")

st.markdown("")

# --- 開始按鈕 ---
if st.button("開始整理"):
    st.success("太好了，我們即將開始第一段探索。")
    st.info("（下一步互動開發中，敬請期待…）")
