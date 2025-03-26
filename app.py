import streamlit as st
import base64

st.set_page_config(
    page_title="永傳 AI 傳承教練 - 首頁",
    page_icon="🌿",
    layout="centered"
)

# Logo base64 顯示
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    logo_base64 = load_logo_base64("logo.png")
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='200'><br>
    </div>
    """, unsafe_allow_html=True)
except:
    st.warning("⚠️ 無法載入 logo.png，請確認檔案存在")

# 品牌標語
st.markdown("""
<div style='text-align: center; font-size: 24px; font-weight: bold; margin-top: 1em;'>
傳承您的影響力
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 16px; margin-top: 0.5em;'>
🌱 每一位家族的掌舵者，都是家族傳承的種子。<br>
我們陪您，讓這份影響力持續茁壯。
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 服務簡介
st.markdown("### 💬 關於「永傳 AI 傳承教練」")
st.markdown("""
這是一套為家族掌舵者量身打造的對話工具，  
幫助您釐清想法、看見方向，從容展開退休與傳承的準備。  

🔸 無需註冊、無壓力體驗  
🔸 透過 AI 對話梳理關鍵思維  
🔸 匯出個人化探索紀錄，作為與家人／顧問對話的起點  
""")

# CTA 按鈕
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("🌿 開始探索傳承藍圖"):
    st.switch_page("pages/coach.py")
st.markdown("</div>", unsafe_allow_html=True)

# 底部資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 12px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a>｜聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
