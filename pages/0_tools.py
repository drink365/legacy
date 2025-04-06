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
st.markdown("### 🗺️ 傳承圖生成器（即將上線）")
st.write("輸入家族成員與資產型態，自動畫出風險與工具對應圖。")
st.button("🔜 敬請期待", key="map_tool")

st.markdown("---")

# 工具 4：保單組合模擬器
st.markdown("### 📦 保單組合模擬器（開發中）")
st.write("根據年齡、預算與年期，自動試算合適的保單配置與現金流。")
st.button("🔜 敬請期待", key="insurance_tool")

st.markdown("---")

# 聯絡與預約
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
