import streamlit as st

st.set_page_config(
    page_title="聯絡我們｜《影響力》傳承策略平台",
    page_icon="📬",
    layout="centered"
)

# 頁首標題
st.markdown("""
<div style='text-align: center;'>
    <h1 style='font-size: 36px;'>📬 聯絡我們</h1>
    <p style='font-size: 16px; color: gray;'>歡迎與《影響力》團隊聯繫，我們樂意陪伴您思考、設計屬於自己的傳承策略。</p>
</div>
""", unsafe_allow_html=True)

# 聯絡資訊區塊
st.markdown("---")
st.markdown("""
### 📧 電子信箱  
若您有任何疑問，或想預約一對一對談，請來信：  
<a href="mailto:123@gracefo.com">123@gracefo.com</a>

### 🌐 官方網站  
更多關於我們的介紹與服務內容，歡迎造訪：  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a>

### 📌 公司資訊  
永傳家族辦公室｜永傳科創股份有限公司  
台北市中山區南京東路二段 101 號 9 樓

---

我們重視每一位用戶的提問與回饋，  
期盼成為您在傳承旅程中的陪伴者與策略夥伴。
""", unsafe_allow_html=True)

# --- 聯絡資訊 ---
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <!-- 根路徑“/”會帶回到 app.py -->
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
