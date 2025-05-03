
import streamlit as st

st.set_page_config(
    page_title="顧問工作台｜《影響力》傳承策略平台",
    page_icon="🧑‍💼",
    layout="centered"
)

# --- 頁首區 ---
st.markdown("""
<div style='text-align: center; margin-top: 1em;'>
    <h2>🧑‍💼 顧問工作台</h2>
    <p style='font-size: 18px;'>這裡是協助客戶進行傳承策略設計的專屬工具箱</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 顧問功能導覽 ---
st.markdown("### 🧰 可使用的顧問模組")

st.markdown("#### 🌿 1. 傳承風格探索")
if st.button("啟動模組", key="go_coach_advisor"):
    st.switch_page("pages/1_coach.py")

st.markdown("#### 🗺️ 2. 資產結構圖工具")
if st.button("啟動模組", key="go_asset_map_advisor"):
    st.switch_page("pages/7_asset_map.py")

st.markdown("#### 📦 3. 保單策略模擬器")
if st.button("啟動模組", key="go_insurance_advisor"):
    st.switch_page("pages/8_insurance_strategy.py")

st.markdown("#### 🧮 4. AI 秒算遺產稅")
if st.button("啟動模組", key="go_tax_advisor"):
    st.switch_page("pages/5_estate_tax.py")

st.markdown("#### 💰 5. 樂活退休試算")
if st.button("啟動模組", key="go_retire_advisor"):
    st.switch_page("pages/6_retirement.py")

st.markdown("#### 🛡️ 6. 傳承風險盤點")
if st.button("啟動模組", key="go_risk_advisor"):
    st.switch_page("pages/9_risk_check.py")

# --- 統一頁尾 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
📧 <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
