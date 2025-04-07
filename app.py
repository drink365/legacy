# --- app.py ---

import streamlit as st
import base64

# --- 頁面設定 ---
st.set_page_config(
    page_title="《影響力》 | 高資產家庭的傳承策略平台",
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

# --- 品牌標語區 ---
st.markdown("""
<div style='text-align: center; margin-top: 2em;'>
    <h1 style='font-size: 36px; font-weight: bold;'>《影響力》</h1>
    <p style='font-size: 24px; color: #333; font-weight: bold; letter-spacing: 0.5px;'>
        高資產家庭的 <span style="color:#006666;">傳承策略平台</span>
    </p>
    <p style='font-size: 18px; color: #888; margin-top: -10px;'>
        讓每一分資源，都成為你影響力的延伸
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 分流入口 ---
st.markdown("### 👥 請選擇您的角色")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🧑‍💼 我是顧問")
    st.write("我想使用《影響力》協助客戶進行規劃")
    if st.button("🔑 進入顧問工作台"):
        st.switch_page("pages/advisor_home.py")

with col2:
    st.markdown("#### 👨‍👩‍👧‍👦 我是客戶")
    st.write("我想釐清自己在傳承上的方向與選擇")
    if st.button("🌿 開始個人探索"):
        st.switch_page("pages/client_home.py")

# --- 頁尾資訊 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
