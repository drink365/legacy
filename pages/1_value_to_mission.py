import streamlit as st

st.set_page_config(
    page_title="從價值觀到任務｜《影響力》傳承策略平台",
    page_icon="🧭",
    layout="centered"
)

# 假設這是前一頁傳來的價值觀清單（正式版需串接 session）
selected_values = st.session_state.get("selected_values", ["家庭安全感", "責任", "影響力"])

# 價值觀對應任務的對照表（可依需求擴充）
value_to_mission = {
    "家庭安全感": "為家人建立穩定生活與風險保障",
    "責任": "清楚安排資產分配與接班結構",
    "影響力": "傳遞理念與精神，影響下一代",
    "自由": "打造財務獨立與彈性退休生活",
    "成就": "確保企業與資產可持續發展",
    "愛": "維繫家族關係與溝通機制",
    "傳統": "傳承價值觀與家風",
    "創新": "為資產創造新用途與新價值"
}

# 根據選擇產生對應任務
matched_missions = []
for v in selected_values:
    if v in value_to_mission:
        matched_missions.append(value_to_mission[v])
matched_missions = list(set(matched_missions))  # 去重

# 顯示
st.markdown("## 🧭 從價值觀，找出您的傳承任務")
st.markdown("根據您剛才選擇的價值觀，我們推測您最在意的任務可能包括：")

if matched_missions:
    for m in matched_missions:
        st.markdown(f"✅ {m}")
else:
    st.warning("目前無法自動判讀任務，請手動勾選")

st.markdown("### 📌 請從下方勾選您最關心的 1～2 項任務：")
selected_missions = st.multiselect(
    "我的傳承任務是...",
    options=matched_missions,
    max_selections=2
)

custom_mission = st.text_input("若您有其他想法，也可以自行填寫：")

if st.button("➡️ 前往策略建議"):
    # 存入 session（方便下一頁接續使用）
    st.session_state.selected_missions = selected_missions
    st.session_state.custom_mission = custom_mission
    st.success("✅ 已儲存您的任務方向，準備前往策略建議頁")
    st.switch_page("pages/2_mission_to_strategy.py")  # 假設下一頁為策略模組頁
