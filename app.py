# app.py
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
<div style='text-align: center; font-size: 28px; font-weight: bold; margin-top: 1em;'>
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

# 快速診斷
st.markdown("### 👣 最近，您有想過這些問題嗎？")
st.markdown("<div style='margin-bottom: -0.5em;'>選一個最有感的選項：</div>", unsafe_allow_html=True)
quiz_option = st.radio("", [
    "我該怎麼安排退休金？",
    "如果我不在了，資產怎麼處理？",
    "接班人真的準備好了嗎？",
    "家人之間的關係好像還沒穩固…"
], index=None)

if quiz_option:
    st.success("✅ 根據您的選項，您非常適合開始探索傳承藍圖！")

# 工具介紹
st.markdown("---")
st.markdown("### 💬 為什麼需要這個工具？")
st.markdown("""
這是一個幫助您整理思緒、掌握方向的智慧探索工具，  
專為家族掌舵者量身打造。

📍 協助您看見真正的關注點  
📍 減輕與家人談論未來安排的壓力  
📍 從心出發，找到適合的傳承路徑  

🕒 **只需 10 分鐘，完成五個探索模組**，即可下載個人化報告，作為與家人或顧問討論的起點。
""")

# CTA 區塊（使用中文名稱作為 switch_page 的參數）
st.markdown("---")
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("🌿 立即開始我的傳承探索"):
    st.switch_page("AI 傳承教練")
st.markdown("</div>", unsafe_allow_html=True)

# 額外導流
st.markdown("---")
st.markdown("### 📬 下一步，想了解我的傳承保障怎麼安排？")
st.markdown("""
💡 歡迎預約 1 對 1 對談，我們將依照您的探索結果，提供專屬傳承與保險建議。  
👉 <a href="mailto:123@gracefo.com?subject=預約家族傳承規劃" target="_blank">點我寄信預約對談</a>
""", unsafe_allow_html=True)

# 底部資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 13px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
