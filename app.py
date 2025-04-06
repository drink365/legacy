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

# CTA：啟動探索
st.markdown("### 🌿 我該從哪裡開始？")
st.markdown("10 分鐘探索流程，陪您釐清思緒、看見方向")
if st.button("🚀 啟動傳承探索教練"):
    st.session_state.start_from_home = True
    st.switch_page("pages/1_coach.py")

# 小工具區標題與收合
st.markdown("---")
st.markdown("### 🧰 永傳家辦小工具")
with st.expander("📦 點我展開工具列表"):
    st.markdown("#### 🔸 AI秒算遺產稅")
    st.write("快速估算您的遺產稅額與現金缺口，為稅務風險提前布局。")
    if st.button("開始試算", key="tax_tool"):
        st.switch_page("pages/5_estate_tax.py")

    st.markdown("#### 🔸 傳承圖生成器（即將上線）")
    st.write("輸入家族成員與資產型態，立即畫出風險與工具對應的視覺地圖。")
    st.button("敬請期待", key="map_tool")

    st.markdown("#### 🔸 保單組合模擬器（開發中）")
    st.write("根據年齡、預算與繳費年期，自動試算合適的保單配置與現金流模型。")
    st.button("敬請期待", key="insurance_tool")

    st.markdown("#### 🔸 樂活退休試算器（開發中）")
    st.write("估算您未來30年生活＋醫療＋長照支出，預測缺口，安心規劃未來。")
    st.button("敬請期待", key="retirement_tool")

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
