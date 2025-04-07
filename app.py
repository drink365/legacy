import streamlit as st
import base64
import os
from modules.lang_utils import set_language, get_text as _

# --- 自動設語言（優先讀取網址參數，再讀取 session） ---
query_lang = st.query_params.get("lang")
if query_lang:
    set_language(query_lang)
elif "language" not in st.session_state:
    set_language("zh-TW")

# --- 語言切換選單 ---
lang_display = {
    "zh-TW": "繁體中文",
    "en": "English",
    "zh-CN": "简体中文"
}

with st.sidebar:
    selected_lang = st.selectbox("🌐 語言 / Language", options=list(lang_display.keys()),
                                  format_func=lambda x: lang_display[x],
                                  index=list(lang_display.keys()).index(st.session_state.language))
    if selected_lang != st.session_state.language:
        set_language(selected_lang)
        st.rerun()

# --- 頁面設定 ---
st.set_page_config(
    page_title=_("page_title"),
    page_icon="🌿",
    layout="centered"
)

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
    st.warning("⚠️ 無法載入 logo.png，請確認檔案存在")

# --- 標語區 ---
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>{_('title')}</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        {_('subtitle')}
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        {_('slogan')}
    </p>
</div>
""", unsafe_allow_html=True)

# --- 開場語 ---
st.markdown(f"""
<div style='text-align: center; margin-top: 3em; font-size: 18px; line-height: 1.8;'>
    {_('opening')}
</div>
""", unsafe_allow_html=True)

# --- 三大價值主張 ---
st.markdown("""
<div style='display: flex; justify-content: center; gap: 40px; margin-top: 3em; flex-wrap: wrap;'>
    <div style='width: 280px; text-align: center;'>
        <h3>🏛️ {_('pillar1_title')}</h3>
        <p>{_('pillar1_text')}</p>
    </div>
    <div style='width: 280px; text-align: center;'>
        <h3>🛡️ {_('pillar2_title')}</h3>
        <p>{_('pillar2_text')}</p>
    </div>
    <div style='width: 280px; text-align: center;'>
        <h3>🌱 {_('pillar3_title')}</h3>
        <p>{_('pillar3_text')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 分流入口按鈕 ---
st.markdown("---")
st.markdown(f"### {_('choose_identity')}")
col1, col2 = st.columns(2)
with col1:
    if st.button("👤 " + _('client_button')):
        st.switch_page("pages/client_home.py")
with col2:
    if st.button("🧑‍💼 " + _('advisor_button')):
        st.switch_page("pages/advisor_home.py")

# --- 頁尾資訊 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室 <a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
