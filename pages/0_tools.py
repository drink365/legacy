import streamlit as st

st.set_page_config(
    page_title="永傳家辦小工具",
    page_icon="🧰",
    layout="centered"
)

st.markdown("""
<div style='text-align: center;'>
    <h1>🧰 永傳家辦小工具</h1>
    <p style='font-size: 18px;'>集合實用工具，幫助您掌握傳承與退休的每一步</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 工具 1：樂活退休試算器
st.markdown("### 💰 樂活退休試算器")
st.write("估算未來30年生活＋醫療＋長照支出與缺口，安心規劃未來。")
if st.button("👉 前往試算：樂活退休", key="go_retirement"):
    st.switch_page("pages/6_retirement.py")

st.markdown("---")

# 工具 2：AI秒算遺產稅
st.markdown("### 🧮 AI秒算遺產稅")
st.write("快速估算您的遺產稅額與現金缺口，為稅務風險提前布局。")
if st.button("👉 前往試算：遺產稅", key="go_tax"):
    st.switch_page("pages/5_estate_tax.py")

st.markdown("---")

# 工具 3：傳承圖生成器
st.markdown("### 🗺️ 傳承圖生成器")
st.write("輸入家族成員與資產型態，自動畫出風險與工具對應圖。")
if st.button("👉 開始使用：傳承圖生成器", key="map_tool"):
    st.switch_page("pages/7_asset_map.py")

st.markdown("---")

# 工具 4：保單策略規劃
st.markdown("### 📦 保單策略規劃")
st.write("依人生任務與資產結構，設計最適保單配置與稅源架構。")
if st.button("👉 開始設計：保單策略", key="insurance_tool"):
    st.switch_page("pages/8_insurance_strategy.py")

st.markdown("---")

# 聯絡與預約
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
