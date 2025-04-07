import streamlit as st

# --- 頁面設定 ---
st.set_page_config(
    page_title="探索工具箱 | 影響力平台",
    page_icon="🧰",
    layout="centered"
)

# --- 頁首標題區塊 ---
st.markdown("""
<div style='text-align: center;'>
    <h1>🧰 探索工具箱</h1>
    <p style='font-size: 18px;'>讓規劃變得更直覺，也更安心</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 工具 1 ---
st.markdown("### 💰 樂活退休試算器")
st.write("預估未來30年生活＋醫療＋長照支出與缺口，規劃安心的退休生活。")
if st.button("👉 前往試算：樂活退休", key="go_retirement"):
    st.switch_page("pages/6_retirement.py")

st.markdown("---")

# --- 工具 2 ---
st.markdown("### 🧮 AI秒算遺產稅")
st.write("快速估算遺產稅與現金缺口，提前準備稅源與保全架構。")
if st.button("👉 前往試算：遺產稅", key="go_tax"):
    st.switch_page("pages/5_estate_tax.py")

st.markdown("---")

# --- 工具 3 ---
st.markdown("### 🗺️ 資產結構圖")
st.write("輸入六大類資產，視覺化呈現風險集中與傳承建議。")
if st.button("👉 開始建立：資產結構圖", key="map_tool"):
    st.switch_page("pages/7_asset_map.py")

st.markdown("---")

# --- 工具 4 ---
st.markdown("### 📦 保單策略設計")
st.write("根據年齡、目標與預算，模擬最適保單組合與保障結構。")
if st.button("👉 啟動設計：保單策略", key="insurance_tool"):
    st.switch_page("pages/8_insurance_strategy.py")

# --- 頁尾資訊 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
