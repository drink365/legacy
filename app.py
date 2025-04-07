import streamlit as st
import base64
from modules.lang_utils import set_language, get_text as _

# 頁面基本設定
st.set_page_config(
    page_title="《影響力》 | 高資產家庭的傳承策略平台",
    page_icon="🌿",
    layout="centered"
)

# 初始化語言
if "app_language" not in st.session_state:
    st.session_state.app_language = "zh-TW"

# 多語系切換邏輯
lang_changed = set_language()
if lang_changed:
    st.success("🌐 語言已切換，重新整理中...")
    st.experimental_rerun()

# 顯示 LOGO（使用 base64 轉換）
def load_logo_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = load_logo_base64("logo.png")

st.markdown(f"""
<div style='text-align: center;'>
    <img src='data:image/png;base64,{logo_base64}' width='200'/>
</div>
""", unsafe_allow_html=True)

# 主標語區
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>《{_('impact_title')}》</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        {_('impact_subtitle')}
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        {_('impact_tagline')}
    </p>
</div>
""", unsafe_allow_html=True)

# 使用者分流按鈕
st.markdown("---")
st.markdown(f"### 👤 {_('choose_user_type')}")

col1, col2 = st.columns(2)
with col1:
    if st.button(f"🧑‍💼 {_('for_advisors')}", use_container_width=True):
        st.switch_page("pages/advisor_home.py")
with col2:
    if st.button(f"🏠 {_('for_clients')}", use_container_width=True):
        st.switch_page("pages/client_home.py")

# 頁尾資訊
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《{_('impact_title')}》{_('platform_footer')}｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
📧 <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
