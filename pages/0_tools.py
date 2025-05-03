
import streamlit as st

# --- 頁面設定 ---
    page_title="《影響力》探索工具箱",
    page_icon="🧰",
    layout="centered"
)

# --- 頁首標題區塊 ---
st.markdown("""
<div style='text-align: center; margin-top: 1em;'>
    <h2>🧰《影響力》探索工具箱</h2>
    <p style='font-size: 18px; color: #555;'>傳承規劃的每一步，都有工具陪伴你設計</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- 工具 1：傳承風險盤點 ---
st.markdown("### 🛡️ 傳承風險盤點")
st.markdown("**Q：我們家目前有哪些傳承風險？**")
st.write("從六大關鍵問題快速盤點風險，對應建議與行動優先順序。")
if st.button("👉 開始檢視：風險盤點", key="risk_tool"):
    st.switch_page("9_risk_check.py")

st.markdown("---")

# --- 工具 2：傳承風格探索 ---
st.markdown("### 🧭 傳承風格探索")
st.markdown("**Q：我的風格適合什麼樣的傳承策略？**")
st.write("了解自己在傳承規劃中的角色定位與溝通風格，找到最適起點。")
if st.button("👉 開始測驗：風格探索", key="coach_tool"):
    st.switch_page("1_coach.py")

st.markdown("---")

# --- 工具 3：樂活退休試算器 ---
st.markdown("### 💰 樂活退休試算器")
st.markdown("**Q：如果我現在退休，資產夠用嗎？**")
st.write("預估未來 30 年生活、醫療與長照支出，看見潛在缺口。")
if st.button("👉 前往試算：樂活退休", key="go_retirement"):
    st.switch_page("6_retirement.py")

st.markdown("---")

# --- 工具 4：AI秒算遺產稅 ---
st.markdown("### 🧮 AI秒算遺產稅")
st.markdown("**Q：萬一我離開，資產會產生多少稅？**")
st.write("快速試算遺產稅與現金缺口，提早準備傳承資金。")
if st.button("👉 前往試算：遺產稅", key="go_tax"):
    st.switch_page("5_estate_tax.py")

st.markdown("---")

# --- 工具 5：資產結構圖 ---
st.markdown("### 🗺️ 資產結構圖")
st.markdown("**Q：我的資產分布合理嗎？風險集中在哪裡？**")
st.write("輸入六大類資產，生成視覺化風險圖與建議摘要。")
if st.button("👉 建立分析：資產結構圖", key="map_tool"):
    st.switch_page("7_asset_map.py")

st.markdown("---")

# --- 工具 6：保單策略設計 ---
st.markdown("### 📦 保單策略設計")
st.markdown("**Q：如何設計出最適合我的保障組合？**")
st.write("依目標、預算與年齡，配置專屬保單與稅務策略。")
if st.button("👉 啟動設計：保單策略", key="insurance_tool"):
    st.switch_page("8_insurance_strategy.py")

# --- 統一頁尾資訊 ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室 <a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
