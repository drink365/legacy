# --- pages/client_home.py ---

import streamlit as st
from modules.lang_utils import get_text as _, set_language

# 初始化語言
set_language()

# 頁面設定
st.set_page_config(
    page_title=_("client_home_title"),
    page_icon="🌿",
    layout="centered"
)

# --- 頁首區 ---
st.markdown(f"""
<div style='text-align: center;'>
    <h2>🌿 {_('client_home_welcome')}</h2>
    <p style='font-size: 18px;'>{_('client_home_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 使用者導引 ---
st.markdown(f"### 🧭 {_('client_home_start_title')}")

st.markdown(f"#### 🔍 1. {_('client_home_step1_title')}")
st.write(_( "client_home_step1_desc"))
if st.button("👉 " + _("client_home_step1_btn")):
    st.switch_page("pages/1_coach.py")

st.markdown(f"#### 💰 2. {_('client_home_step2_title')}")
st.write(_( "client_home_step2_desc"))
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 " + _("client_home_retirement_btn")):
        st.switch_page("pages/6_retirement.py")
with col2:
    if st.button("🧮 " + _("client_home_tax_btn")):
        st.switch_page("pages/5_estate_tax.py")

st.markdown(f"#### 📦 3. {_('client_home_step3_title')}")
st.write(_( "client_home_step3_desc"))
col3, col4 = st.columns(2)
with col3:
    if st.button("🗺️ " + _("client_home_map_btn")):
        st.switch_page("pages/7_asset_map.py")
with col4:
    if st.button("📦 " + _("client_home_insurance_btn")):
        st.switch_page("pages/8_insurance_strategy.py")

# --- 頁尾 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《{_('brand_name')}》{_('brand_tagline')}｜{_('brand_company')}<br>
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
📧 <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
