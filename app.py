import streamlit as st
import base64
import os
from modules.lang_utils import set_language, get_text as _

# 設定頁面屬性
st.set_page_config(
    page_title="《影響力》| 傳承策略平台",
    page_icon="🌿",
    layout="centered"
)

# 啟用語言設定
set_language()

# 語言選擇下拉選單
lang_display = {
    "zh-TW": "繁體中文",
    "en": "English",
    "zh-CN": "简体中文"
}

selected_lang = st.selectbox(
    "🌐 選擇語言｜Language",
    options=list(lang_display.keys()),
    format_func=lambda x: lang_display[x],
    index=list(lang_display.keys()).index(st.session_state.language)
)

# 若語言切換，儲存並重新載入
if selected_lang != st.session_state.language:
    st.session_state.language = selected_lang
    st.rerun()

# 顯示 logo
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_path = "logo.png"
if os.path.exists(logo_path):
    logo_base64 = load_logo_base64(logo_path)
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='200'/>
    </div>
    """, unsafe_allow_html=True)

# 主標題與副標語
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>{_('main_title')}</h1>
    <p style='font-size: 20px; color: #555;'>{_('main_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# 使用者分流
st.markdown("---")
st.markdown(f"### {_('entry_prompt')}")

col1, col2 = st.columns(2)

with col1:
    if st.button(f"👨‍👩‍👧‍👦 {_('client_entry_btn')}", use_container_width=True):
        st.switch_page("pages/client_home.py")

with col2:
    if st.button(f"🧑‍💼 {_('advisor_entry_btn')}", use_container_width=True):
        st.switch_page("pages/advisor_home.py")

# 頁尾資訊
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《{_('brand_name')}》{_('brand_slogan')}｜永傳家族辦公室 <a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
📧 {_('contact_email')}：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
