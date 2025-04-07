import streamlit as st
import base64
from modules.lang_utils import set_language, get_text as _

# 頁面設定
st.set_page_config(
    page_title="《影響力》 | 傳承策略平台",
    page_icon="🌿",
    layout="centered"
)

# --- 語言選擇（顯示在側邊欄） ---
with st.sidebar:
    st.markdown("### 🌐 語言選擇 Language")
    set_language()

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

# --- 品牌標語區 ---
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

# --- 角色分流 ---
st.markdown("---")
st.markdown(f"## {_('choose_identity')}")
col1, col2 = st.columns(2)
with col1:
    if st.button(f"👤 {_('client')}"):
        st.switch_page("pages/client_home.py")
with col2:
    if st.button(f"👔 {_('advisor')}"):
        st.switch_page("pages/advisor_home.py")

# --- 頁尾資訊 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室 <br>
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
📧 <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
