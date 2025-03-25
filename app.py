import streamlit as st
import base64

# 頁面設定
st.set_page_config(
    page_title="永傳 AI 傳承教練 - 首頁",
    page_icon="🌿",
    layout="centered"
)

# Logo base64 顯示
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 嘗試載入 logo
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

# 品牌精神
st.markdown("""
<div style='text-align: center; font-size: 16px; margin-top: 0.5em;'>
🌱 每一位家族的掌舵者，都是家族傳承的種子。<br>
我們陪您，讓這份影響力持續茁壯。
</div>
""", unsafe_allow_html=True)

# 心情引導
st.markdown("""
<div style='text-align: center; font-size: 14px; margin-top: 1.2em; color: #555;'>
也許，您正在思考未來該怎麼交棒、何時退休、怎麼安排資產……<br>
這裡是一個讓思緒慢慢清晰的起點。
</div>
""", unsafe_allow_html=True)

# 分隔線
st.markdown("---")

# 工具簡介
st.markdown("### 💬 關於「永傳 AI 傳承教練」")
st.markdown("""
👀 **幫助您釐清重要的家族思維**  
這是一套為「家族掌舵者」設計的對話工具，讓您思考如何交棒、如何安排、如何說出心聲。

🧭 **AI 陪您慢慢梳理方向**  
從提問、探索、再到策略建議，幫助您看清自己的優先順序與未來方向。

📄 **產出專屬於您的探索紀錄**  
最終您可下載一份個人報告，作為與家人或顧問對話的起點。
""")

# 行動引導
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; font-size: 14px;'>準備好了嗎？從這裡展開屬於您的傳承藍圖。</div>", unsafe_allow_html=True)

# CTA 按鈕
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("🌿 開始探索傳承藍圖"):
    st.switch_page("app.py")  # 確保 app.py 與 landing.py 在正確位置
st.markdown("</div>", unsafe_allow_html=True)

# 底部資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 12px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a>｜聯絡信箱：123@gracefo.com<br>
以人為本，陪您思考未來。
</div>
""", unsafe_allow_html=True)
