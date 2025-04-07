import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from modules.lang_utils import set_language, get_text as _

# 設定頁面基本資訊
st.set_page_config(
    page_title="《影響力》｜高資產家庭的傳承策略平台",
    page_icon="🌿",
    layout="centered"
)

# 語言選擇
lang = st.selectbox("🌐 請選擇語言 | Language | 语言", ["繁體中文", "English", "简体中文"])
set_language(lang)

# 顯示 LOGO
st.image("logo.png", width=220)

# 品牌主標題
st.markdown(f"""
<div style='text-align: center; margin-top: 1em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>{_('impact_platform_title')}</h1>
    <p style='font-size: 20px; color: #666;'>{_('impact_platform_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 角色分流選擇
st.markdown(f"### 👤 {_('who_are_you')}")
option = st.radio(
    label="",
    options=[_("client_identity"), _("advisor_identity")],
    horizontal=True
)

if option == _("client_identity"):
    if st.button(_("enter_client")):
        st.switch_page("pages/client_home.py")
else:
    if st.button(_("enter_advisor")):
        st.switch_page("pages/advisor_home.py")

# 頁尾資訊
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
{_('platform_footer')}｜<a href="https://gracefo.com" target="_blank">gracefo.com</a><br>
📧 <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
