# --- pages/advisor_home.py ---

import streamlit as st

st.set_page_config(
    page_title="我是顧問｜《影響力》傳承策略平台",
    page_icon="🧑‍💼",
    layout="centered"
)

# --- 頁首區 ---
st.markdown("""
<div style='text-align: center;'>
    <h2>🧑‍💼 顧問工作台</h2>
    <p style='font-size: 18px;'>這裡是協助客戶進行傳承策略設計的專屬工具箱</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 顧問功能導覽 ---
st.markdown("### 🧰 協助客戶進行策略設計")

st.markdown("#### 👥 1. 引導客戶探索傳承風格")
st.write("使用互動模組，協助客戶釐清價值觀與關注重點。")
if st.button("🌿 啟動傳承探索工具", key="go_coach_advisor"):
    st.switch_page("pages/1_coach.py")

st.markdown("#### 📊 2. 建立資產結構圖")
st.write("輸入資產項目後，自動產出風險建議與圖像報告。")
if st.button("🗺️ 開始資產建構", key="go_asset_map_advisor"):
    st.switch_page("pages/7_asset_map.py")

st.markdown("#### 📦 3. 保單建議模擬器")
st.write("依照預算、年齡與目標，自動生成策略組合與PDF建議書。")
if st.button("📦 啟用保單模擬器", key="go_insurance_advisor"):
    st.switch_page("pages/8_insurance_strategy.py")

st.markdown("#### 🧮 4. 遺產稅與退休試算")
st.write("快速掌握現金缺口與保險／稅源設計依據。")
col1, col2 = st.columns(2)
with col1:
    if st.button("🧮 遺產稅試算", key="go_tax_advisor"):
        st.switch_page("pages/5_estate_tax.py")
with col2:
    if st.button("💰 樂活退休試算", key="go_retire_advisor"):
        st.switch_page("pages/6_retirement.py")

# --- 頁尾 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
