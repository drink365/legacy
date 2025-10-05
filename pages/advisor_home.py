import streamlit as st
from app_config import ensure_page_config
ensure_page_config()
# --- Force-hide Streamlit sidebar & its toggle (applies to this page) ---
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)
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

st.markdown("#### 📊 2. 建立資產結構圖與現金流模擬")
st.write("輸入資產項目後，自動產出風險建議與圖像報告。")
if st.button("🗺️ 開始資產建構", key="go_asset_map_advisor"):
    st.switch_page("pages/7_asset_map.py")

st.markdown("#### 📦 3. 保單建議模擬器")
st.write("依照預算、年齡與目標，自動生成策略組合與PDF建議書。")
if st.button("📦 啟用保單模擬器", key="go_insurance_advisor"):
    st.switch_page("pages/8_insurance_strategy.py")

st.markdown("#### 🛡️ 4. 傳承風險盤點工具")
st.write("協助客戶從六大面向盤點風險，導入後續顧問規劃建議。")
if st.button("🛡️ 啟用風險盤點工具", key="go_risk_check_advisor"):
    st.switch_page("pages/9_risk_check.py")

st.markdown("#### 🧮 5. 遺產稅與退休試算")
st.write("快速掌握現金缺口與保險／稅源設計依據。")
col1, col2 = st.columns(2)
with col1:
    if st.button("🧮 AI秒算遺產稅", key="go_tax_advisor"):
        st.switch_page("pages/5_estate_tax.py")
with col2:
    if st.button("💰 樂活退休試算", key="go_retire_advisor"):
        st.switch_page("pages/6_retirement.py")

# 新增: 不動產稅負試算連結
st.markdown("#### 🏠 6. 不動產稅負試算")
st.write("協助客戶快速試算未來不動產買賣或贈與/繼承的稅負情境。")
if st.button("🏠 AI秒算房產傳承稅負", key="go_real_estate_tax_advisor"):
    st.switch_page("pages/10_property.py")

# --- 聯絡資訊 ---
st.markdown("---")
st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
      <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
      <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
      <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
