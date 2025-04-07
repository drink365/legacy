import streamlit as st
import base64

# --- 頁面設定 ---
st.set_page_config(
    page_title="影響力｜高資產家庭的傳承策略平台",
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
    <h1 style='font-size: 48px; font-weight: bold;'>影響力</h1>
    <p style='font-size: 20px; color: #555;'>高資產家庭的傳承策略平台</p>
</div>
""", unsafe_allow_html=True)

# --- 品牌開場語 ---
st.markdown("""
<div style='text-align: center; margin-top: 3em; font-size: 18px; line-height: 1.8;'>
    你的人生，不只是擁有，更是一種影響力。<br>
    我們陪你設計每一分資源的去向，<br>
    讓它能守護最重要的人，延續你真正的價值。
</div>
""", unsafe_allow_html=True)

# --- 三大價值主張 ---
st.markdown("""
<div style='display: flex; justify-content: center; gap: 40px; margin-top: 3em;'>
    <div style='width: 30%; text-align: center;'>
        <h3>🏛️ 富足結構</h3>
        <p>為資產設計流動性與穩定性，讓財富更有效率地守護人生階段。</p>
    </div>
    <div style='width: 30%; text-align: center;'>
        <h3>🛡️ 風險預備</h3>
        <p>從保單、稅源到信託制度，設計資產的防禦系統與轉移機制。</p>
    </div>
    <div style='width: 30%; text-align: center;'>
        <h3>🌱 價值傳遞</h3>
        <p>不只是金錢，更是精神、信任與選擇，成就跨世代的連結。</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 模組導覽 ---
st.markdown("---")
st.markdown("### 🧰 我可以從哪裡開始？")

st.markdown("#### 🔸 傳承風格探索")
st.write("找出你適合的傳承角色與價值定位")
if st.button("立即開始探索", key="go_coach"):
    st.switch_page("pages/1_coach.py")

st.markdown("#### 🔸 資產結構圖")
st.write("輸入六大類資產，看懂風險集中與稅源佈局")
if st.button("開始建立資產圖", key="go_map"):
    st.switch_page("pages/7_asset_map.py")

st.markdown("#### 🔸 遺產稅快速試算")
st.write("估算未來的現金缺口與稅源準備")
if st.button("進入試算工具", key="go_tax"):
    st.switch_page("pages/5_estate_tax.py")

st.markdown("#### 🔸 保單策略設計")
st.write("根據任務與資源，設計最適保單組合")
if st.button("啟動保單設計", key="go_insurance"):
    st.switch_page("pages/8_insurance_strategy.py")

# --- 聯絡資訊 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
