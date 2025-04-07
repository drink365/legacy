import streamlit as st
import base64
from modules.lang_utils import set_language, get_text as _

# --- 頁面設定 ---
st.set_page_config(
    page_title=_("app_title"),
    page_icon="🌿",
    layout="centered"
)

# --- 語言切換 ---
prev_lang = st.session_state.get("app_language", "zh-TW")
set_language()
curr_lang = st.session_state.get("app_language")
if prev_lang != curr_lang:
    st.experimental_rerun()

# --- 讀取 logo ---
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    logo_base64 = load_logo_base64("logo.png")
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='200'><br>
    </div>
    """, unsafe_allow_html=True)
except:
    st.warning(_("logo_missing_warning"))

# --- 品牌標語區 ---
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>{_('platform_name')}</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        {_('platform_slogan')}
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        {_('platform_description')}
    </p>
</div>
""", unsafe_allow_html=True)

# --- 使用者分流入口 ---
st.markdown("---")
st.markdown(f"### {_('who_are_you')}")

col1, col2 = st.columns(2)

with col1:
    if st.button(_("for_clients")):
        st.switch_page("pages/client_home.py")

with col2:
    if st.button(_("for_advisors")):
        st.switch_page("pages/advisor_home.py")

# --- 頁尾資訊 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
{_('footer_organization')}｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
{_('footer_contact')}：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
