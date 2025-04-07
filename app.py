import streamlit as st
import base64
from modules.lang_utils import set_language, get_text as _

# 頁面設定
st.set_page_config(
    page_title="《影響力》 | 高資產家庭的傳承策略入口",
    page_icon="🌿",
    layout="centered"
)

# 語言選擇器
lang = st.selectbox("🌐 Language 語言選擇 / Language", ["繁體中文", "English", "简体中文"])
set_language(lang)

# 讀取 logo
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
    st.warning(_("warn_logo"))

# 標題與標語
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>{_('title_platform')}</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        {_('subtitle_platform')}
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        {_('slogan')}
    </p>
</div>
""", unsafe_allow_html=True)

# 開場語
st.markdown(f"""
<div style='text-align: center; margin-top: 3em; font-size: 18px; line-height: 1.8;'>
    {_('intro_text')}
</div>
""", unsafe_allow_html=True)

# 三大價值主張
st.markdown(f"""
<div style='display: flex; justify-content: center; gap: 40px; margin-top: 3em; flex-wrap: wrap;'>
    <div style='width: 280px; text-align: center;'>
        <h3>🏛️ {_('value_structure')}</h3>
        <p>{_('value_structure_text')}</p>
    </div>
    <div style='width: 280px; text-align: center;'>
        <h3>🛡️ {_('value_risk')}</h3>
        <p>{_('value_risk_text')}</p>
    </div>
    <div style='width: 280px; text-align: center;'>
        <h3>🌱 {_('value_legacy')}</h3>
        <p>{_('value_legacy_text')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 使用者分流選擇
st.markdown("---")
st.markdown(f"### {_('choose_identity')}")
col1, col2 = st.columns(2)
with col1:
    if st.button("🙋 " + _("identity_client")):
        st.switch_page("pages/client_home.py")
with col2:
    if st.button("👩‍💼 " + _("identity_advisor")):
        st.switch_page("pages/advisor_home.py")

# 頁尾資訊
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室<br>
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
{_('contact_email')} <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
