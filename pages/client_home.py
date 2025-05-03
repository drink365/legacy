
import streamlit as st

st.set_page_config(
    page_title="我是客戶｜《影響力》傳承策略平台",
    page_icon="🙋",
    layout="centered"
)

# --- 頁首區 ---
st.markdown("""
<div style='text-align: center; margin-top: 1em;'>
    <h2>🙋 客戶專屬入口</h2>
    <p style='font-size: 18px;'>您可以依需求探索合適的傳承策略模組</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 客戶功能選單 ---
st.markdown("### 🌿 傳承風格探索")
st.write("透過引導互動，釐清您的價值觀與傳承優先順序。")
if st.button("🔍 啟動風格探索", key="go_coach_client"):
    st.switch_page("pages/1_coach.py")

st.markdown("### 🧰 傳承工具試算")
st.write("您可進一步使用退休／遺產稅／風險盤點等模組。")
if st.button("🧮 前往工具箱", key="go_toolbox_client"):
    st.switch_page("pages/0_tools.py")

st.markdown("### 📞 預約顧問諮詢")
st.write("若您希望獲得專人協助與策略建議，歡迎預約。")
if st.button("📩 填寫預約表單", key="go_contact_client"):
    st.switch_page("pages/4_contact.py")

# --- 統一頁尾 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
📧 <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
