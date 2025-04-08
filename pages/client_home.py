import streamlit as st
from modules.lang_utils import set_language, get_text as _

# 🔰 載入語言
current_lang = st.session_state.get("language", "zh-TW")
set_language(current_lang)

# 頁面設定
st.set_page_config(
    page_title=_("client_home.title"),
    page_icon="🌿",
    layout="centered"
)

# --- 頁首區 ---
st.markdown(f"""
<div style='text-align: center;'>
    <h2>🌿 {_('client_home.heading')}</h2>
    <p style='font-size: 18px;'>{_('client_home.subheading')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 使用者導引 ---
st.markdown(f"### 🧭 {_('client_home.section_intro')}")

# 傳承風格探索
st.markdown(f"#### 🔍 1. {_('client_home.part1.title')}")
st.write(_("client_home.part1.desc"))
if st.button(_("client_home.part1.button")):
    st.switch_page("pages/1_coach.py")

# 試算工具
st.markdown(f"#### 💰 2. {_('client_home.part2.title')}")
st.write(_("client_home.part2.desc"))
col1, col2 = st.columns(2)
with col1:
    if st.button(_("client_home.part2.btn_retire")):
        st.switch_page("pages/6_retirement.py")
with col2:
    if st.button(_("client_home.part2.btn_tax")):
        st.switch_page("pages/5_estate_tax.py")

# 資產與保單模組
st.markdown(f"#### 📦 3. {_('client_home.part3.title')}")
st.write(_("client_home.part3.desc"))
col3, col4 = st.columns(2)
with col3:
    if st.button(_("client_home.part3.btn_asset")):
        st.switch_page("pages/7_asset_map.py")
with col4:
    if st.button(_("client_home.part3.btn_insurance")):
        st.switch_page("pages/8_insurance_strategy.py")

# --- 頁尾 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
{_('contact.email_label')}：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
