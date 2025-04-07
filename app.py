import streamlit as st
import base64

st.set_page_config(
    page_title="永傳家族傳承教練 - 首頁",
    page_icon="🌿",
    layout="centered"
)

# Logo base64 顯示
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

# 品牌標語
st.markdown("""
<div style='text-align: center; font-size: 28px; font-weight: bold; margin-top: 1em;'>
傳承您的影響力
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 16px; margin-top: 0.5em;'>
🌱 每一位家族的掌舵者，都是家族傳承的種子。<br>
我們陪您，讓這份影響力持續茁壯。
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 快速導入探索流程
st.markdown("### 👣 最近，您有想過這些問題嗎？")
st.markdown("<div style='margin-bottom: -0.5em;'>選一個最有感的選項：</div>", unsafe_allow_html=True)
quiz_option = st.radio("", [
    "我該怎麼安排退休金？",
    "如果我不在了，資產怎麼處理？",
    "接班人真的準備好了嗎？",
    "家人之間的關係好像還沒穩固…"
], index=None)

if quiz_option:
    st.success("✅ 根據您的選項，您非常適合開始探索傳承藍圖！")

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("🌿 立即開始我的傳承探索"):
    st.switch_page("pages/1_coach.py")
st.markdown("</div>", unsafe_allow_html=True)

# 小工具懶人包
st.markdown("---")
st.markdown("### 🧰 永傳家辦小工具")

st.markdown("#### 🔸 AI秒算遺產稅")
st.write("快速估算您的遺產稅額與現金缺口，為稅務風險提前布局。")
if st.button("開始試算", key="tax_tool"):
    st.switch_page("pages/5_estate_tax.py")

st.markdown("#### 🔸 樂活退休試算器")
st.write("估算您未來 30 年生活＋醫療＋長照支出，預測缺口，安心規劃未來。")
if st.button("開始試算", key="retirement_tool"):
    st.switch_page("pages/6_retirement.py")

st.markdown("#### 🔸 傳承圖生成器")
st.write("輸入家族成員與資產型態，立即畫出風險與工具對應的視覺地圖。")
if st.button("開始探索", key="map_tool"):
    st.switch_page("pages/7_asset_map.py")

st.markdown("#### 🔸 保單策略規劃")
st.write("依人生任務與資產結構，設計最適保單配置與稅源架構。")
if st.button("開始設計", key="insurance_tool"):
    st.switch_page("pages/8_insurance_strategy.py")

# 行動導流
st.markdown("---")
st.markdown("### 📬 下一步，想了解我的傳承保障怎麼安排？")
st.markdown("""
💡 歡迎預約 1 對 1 對談，我們將依照您的探索結果，提供專屬傳承與保險建議。  
👉 <a href="mailto:123@gracefo.com?subject=預約家族傳承規劃" target="_blank">點我寄信預約對談</a>
""", unsafe_allow_html=True)

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
