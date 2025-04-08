import streamlit as st

st.set_page_config(
    page_title="我是客戶｜《影響力》傳承策略平台",
    page_icon="🌿",
    layout="centered"
)

# --- 頁首區 ---
st.markdown("""
<div style='text-align: center;'>
    <h2>🌿 歡迎使用《影響力》</h2>
    <p style='font-size: 18px;'>這裡是專屬高資產家庭的傳承策略起點</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 使用者導引 ---
st.markdown("### 🧭 請問您想從哪裡開始？")

st.markdown("#### 🔍 1. 找出我的傳承風格")
st.write("透過小測驗與引導式提問，幫助您釐清內心想法與優先順序。")
if st.button("👉 開始風格探索"):
    st.switch_page("pages/1_coach.py")

st.markdown("#### 💰 2. 試算退休與稅務需求")
st.write("預估退休支出、遺產稅缺口，看見未來現金需求與規劃起點。")
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 樂活退休試算"):
        st.switch_page("pages/6_retirement.py")
with col2:
    if st.button("🧮 遺產稅快速試算"):
        st.switch_page("pages/5_estate_tax.py")

st.markdown("#### 📦 3. 保單與資產結構設計")
st.write("輸入資產類別，立即看見風險圖與保單建議。")
col3, col4 = st.columns(2)
with col3:
    if st.button("🗺️ 資產結構圖"):
        st.switch_page("pages/7_asset_map.py")
with col4:
    if st.button("📦 保單策略設計"):
        st.switch_page("pages/8_insurance_strategy.py")

# --- 頁尾 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
