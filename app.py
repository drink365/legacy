
import streamlit as st

st.set_page_config(page_title="《影響力》傳承策略平台", layout="centered")

st.markdown("<h1 style='text-align: center;'>🌿 歡迎來到《影響力》傳承策略平台</h1>", unsafe_allow_html=True)
st.markdown("讓我們陪您一起打造有系統、有溫度的家族傳承規劃。")

st.markdown("## 🔍 精選工具入口")

# 工具卡片區塊
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧭 傳承風格探索")
    st.markdown("了解您在家族傳承中的思維偏好與策略風格。")
    st.page_link("pages/1_coach.py", label="開始測驗 ➜")

with col2:
    st.markdown("### 🛡️ 傳承風險盤點")
    st.markdown("快速檢視潛在風險，立即找出傳承漏洞與改善重點。")
    st.page_link("pages/9_risk_check.py", label="立即盤點 ➜")

st.markdown("---")
st.markdown("### 📚 更多功能陸續更新中...")
st.markdown("- ✅ 遺產稅模擬器")
st.markdown("- 📦 保單策略建議模組")
st.markdown("- 🧭 AI 傳承教練")

st.markdown("<small>設計與維護：永傳家族辦公室｜Grace</small>", unsafe_allow_html=True)
