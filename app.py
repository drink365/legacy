
import streamlit as st

st.set_page_config(page_title="《影響力》傳承策略平台", layout="centered")

st.markdown("<h1 style='text-align: center;'>🌿 歡迎來到《影響力》傳承策略平台</h1>", unsafe_allow_html=True)
st.markdown("""
這是一個為高資產家庭與企業創辦人打造的策略平台，  
讓您用熟悉的方式，安心開啟屬於自己的家族傳承對話。
""")

st.markdown("## 🔍 精選互動工具")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧭 傳承風格探索")
    st.markdown("從價值觀出發，找到最適合您的傳承策略起點。")
    st.page_link("pages/1_coach.py", label="開始測驗 ➜")

with col2:
    st.markdown("### 🛡️ 傳承風險盤點")
    st.markdown("快速檢視潛在風險，釐清資產與法律上的規劃盲點。")
    st.page_link("pages/9_risk_check.py", label="立即盤點 ➜")

st.markdown("## 🔧 進階應用工具")

st.markdown("- 📦 保單策略模擬器")
st.markdown("- 💡 遺產稅即時試算")
st.markdown("- 🤖 AI 傳承教練｜完整陪伴您從資產盤點到策略布局")

st.markdown("<small>設計與維護：永傳家族辦公室｜Grace</small>", unsafe_allow_html=True)
