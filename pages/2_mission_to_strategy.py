import streamlit as st

st.set_page_config(
    page_title="從目標走向策略｜《影響力》平台",
    page_icon="🧭",
    layout="centered"
)

st.markdown("""
<div style='text-align: center;'>
    <h2>🧭 從目標走向策略</h2>
    <p style='font-size: 18px;'>讓我們根據剛剛選出的目標，協助您找到可以起步的行動方向</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 模擬選擇的價值目標（實務上可從 session_state 傳入）
goals = st.session_state.get("selected_values", [
    "我希望退休後仍有影響力",
    "我希望資產能安全傳承給孩子",
    "我希望能預留足夠的醫療與長照資源"
])

# 對應的策略建議資料庫（簡化版）
strategy_map = {
    "我希望退休後仍有影響力": "考慮建立家族治理架構、設定信託條款保有參與權",
    "我希望資產能安全傳承給孩子": "可先盤點資產結構，並考慮搭配遺囑、保單與信託設計",
    "我希望能預留足夠的醫療與長照資源": "建議檢視現有保單保障，並補強現金流型工具，如年金或高現金值保單"
}

st.markdown("### 🎯 您選擇的目標與建議策略：")

for goal in goals:
    with st.expander(f"🎯 {goal}"):
        st.write(strategy_map.get(goal, "（尚未提供建議，請與顧問討論）"))

st.markdown("---")

st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室 <br>
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
