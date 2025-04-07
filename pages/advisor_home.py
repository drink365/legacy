import streamlit as st

st.set_page_config(
    page_title="顧問專區｜《影響力》平台",
    page_icon="🧑‍💼",
    layout="centered"
)

st.markdown("""
<div style='text-align: center;'>
    <h2>🧑‍💼 顧問專區</h2>
    <p style='font-size: 18px;'>專為專業顧問打造的工具與資源中心</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
---

### 🎯 顧問常用工具

- [✅ 傳承風格探索](1_coach)
- [📦 保單策略設計](8_insurance_strategy)
- [🗺️ 資產結構圖](7_asset_map)
- [🧮 AI秒算遺產稅](5_estate_tax)

---

### 📚 教學與案例資源

- [📘 傳承案例分享](2_cases)
- [📥 工具箱總覽](0_tools)

---

### 📬 聯絡與平台資訊

- [🌐 官方網站](https://gracefo.com)
- [📧 聯絡我們](mailto:123@gracefo.com)

<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜《影響力》傳承策略平台
</div>
""", unsafe_allow_html=True)
