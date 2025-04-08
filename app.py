import streamlit as st
import base64
import os
from modules.lang_utils import set_language, get_text as _

# --- 頁面設定 ---
st.set_page_config(
    page_title=_("brand_name") + " | " + _("brand_tagline"),
    page_icon="🌿",
    layout="centered"
)

# --- 語言切換（放在頁首） ---
lang_display = {"zh-TW": "繁體中文", "en": "English", "zh-CN": "简体中文"}
current_lang = st.selectbox(
    "🌐 選擇語言 / Language",
    options=list(lang_display.keys()),
    format_func=lambda x: lang_display[x],
    index=list(lang_display.keys()).index(st.session_state.get("language", "zh-TW"))
)
set_language(current_lang)

# --- 讀取 logo ---
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_path = "logo.png"
if os.path.exists(logo_path):
    logo_base64 = load_logo_base64(logo_path)
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='200'><br>
    </div>
    """, unsafe_allow_html=True)

# --- 品牌標語 ---
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>{_("brand_name")}</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        {_("brand_tagline")}
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        {_("home_subtext") if _("home_subtext") != "home_subtext" else "讓每一分資源，都成為你影響力的延伸"}
    </p>
</div>
""", unsafe_allow_html=True)

# --- 導覽按鈕區 ---
st.markdown("---")
st.markdown("### 🙋 請問您是...")

col1, col2 = st.columns(2)

with col1:
    if st.button("👤 我是客戶"):
        st.switch_page("pages/client_home.py")

with col2:
    if st.button("🧑‍💼 我是顧問"):
        st.switch_page("pages/advisor_home.py")

# --- 頁尾 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《{_("brand_name")}》{_("brand_tagline")}｜{_("brand_company")}<br>
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
