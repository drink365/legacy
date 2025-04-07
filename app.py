import streamlit as st
import sys
import os

# ✅ 加入 modules 模組所在路徑
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

from lang_utils import set_language, get_text as _

# 頁面設定
st.set_page_config(
    page_title=_("《影響力》 | 高資產家庭的傳承策略入口"),
    page_icon="🌿",
    layout="centered"
)

# 語言切換
set_language()

# --- Logo 顯示 ---
try:
    with open("logo.png", "rb") as f:
        logo_data = f.read()
    import base64
    logo_base64 = base64.b64encode(logo_data).decode("utf-8")
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='200'><br>
    </div>
    """, unsafe_allow_html=True)
except:
    st.warning("⚠️ 找不到 logo.png，請確認圖片存在。")

# --- 品牌標語區 ---
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>{_('《影響力》')}</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        {_('高資產家庭的')} <span style="color:#006666;">{_('傳承策略平台')}</span>
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        {_('讓每一分資源，都成為你影響力的延伸')}
    </p>
</div>
""", unsafe_allow_html=True)

# --- 使用者分流入口 ---
st.markdown("---")
st.markdown(f"### 🌱 {_('請問您是？')}")
col1, col2 = st.columns(2)

with col1:
    if st.button(f"👤 {_('我是高資產客戶')}"):
        st.switch_page("pages/client_home.py")

with col2:
    if st.button(f"🧑‍💼 {_('我是傳承顧問 / 業務員')}"):
        st.switch_page("pages/advisor_home.py")

# --- 頁尾資訊 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
