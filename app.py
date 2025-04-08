import streamlit as st
import base64

# 設定頁面
st.set_page_config(
    page_title="《影響力》 | 高資產家庭的傳承策略入口",
    page_icon="🌿",
    layout="centered"
)


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
    st.warning(_("logo_warning"))  # 需在 lang_xx.json 中新增 "logo_warning": "⚠️ 無法載入 logo.png，請確認檔案存在"

# --- 品牌標語區 ---
st.markdown(f"""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>《{_('brand_name')}》</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        {_('brand_subtitle')}
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        {_('brand_slogan')}
    </p>
</div>
""", unsafe_allow_html=True)

# --- 品牌開場語 ---
st.markdown(f"""
<div style='text-align: center; margin-top: 3em; font-size: 18px; line-height: 1.8;'>
    {_('brand_intro_line1')}<br>
    {_('brand_intro_line2')}<br>
    {_('brand_intro_line3')}
</div>
""", unsafe_allow_html=True)

# --- 三大價值主張 ---
st.markdown(f"""
<div style='display: flex; justify-content: center; gap: 40px; margin-top: 3em; flex-wrap: wrap;'>
    <div style='width: 280px; text-align: center;'>
        <h3>🏛️ {_('value_1_title')}</h3>
        <p>{_('value_1_desc')}</p>
    </div>
    <div style='width: 280px; text-align: center;'>
        <h3>🛡️ {_('value_2_title')}</h3>
        <p>{_('value_2_desc')}</p>
    </div>
    <div style='width: 280px; text-align: center;'>
        <h3>🌱 {_('value_3_title')}</h3>
        <p>{_('value_3_desc')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 使用者分流 ---
st.markdown("---")
st.markdown(f"### {_('entry_title')}")
col1, col2 = st.columns(2)

with col1:
    if st.button(f"🙋 {_('client_button')}", use_container_width=True):
        st.switch_page("pages/client_home.py")

with col2:
    if st.button(f"🧑‍💼 {_('advisor_button')}", use_container_width=True):
        st.switch_page("pages/advisor_home.py")

# --- 聯絡資訊 ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; font-size: 14px; color: gray;'>
《{_('brand_name')}》傳承策略平台｜永傳家族辦公室 <a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
📧 <a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
