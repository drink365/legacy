import streamlit as st

# --- 頁面設定 ---
st.set_page_config(page_title="傳承風險盤點測驗", layout="centered")

# --- 標題區 ---
st.markdown("<h1 style='text-align: center;'>🛡️ 傳承風險盤點測驗</h1>", unsafe_allow_html=True)
st.markdown("請依實際情況回答以下問題，我們將快速協助您辨識家族傳承中的潛在風險。")

# --- 題目設定 ---
questions = [
    ("您的父母或長輩是否已立下遺囑？", "未立遺囑 → 恐有未來爭產風險"),
    ("您是否清楚目前家庭資產結構（包含股權、保單、不動產等）？", "資產結構不明 → 傳承規劃難以落實"),
    ("是否有為配偶設計足夠的保障或財產分配安排？", "配偶保障不足 → 老後可能陷入經濟風險"),
    ("您是否已開始規劃稅務影響（如贈與稅、遺產稅）？", "未提前規劃稅務 → 可能產生高額稅負"),
    ("公司股權是否有清楚的接班與移轉安排？", "公司股權未安排 → 恐影響企業穩定與家族關係"),
    ("家庭成員之間是否已共識財產分配方向？", "缺乏共識 → 潛藏親情裂痕與衝突風險")
]

# --- 初始狀態設定 ---
if "risk_quiz_done" not in st.session_state:
    st.session_state.risk_quiz_done = False
if "risk_flags" not in st.session_state:
    st.session_state.risk_flags = []

# --- 填答階段 ---
if not st.session_state.risk_quiz_done:
    for idx, (q, _) in enumerate(questions):
        st.radio(f"{idx+1}. {q}", ["是", "否"], key=f"risk_{idx}")

    if st.button("🔍 產出我的風險清單"):
        flags = []
        for idx, (_, risk) in enumerate(questions):
            answer = st.session_state.get(f"risk_{idx}")
            if answer == "否":
                flags.append(risk)
        st.session_state.risk_flags = flags
        st.session_state.risk_quiz_done = True

# --- 結果顯示階段 ---
else:
    st.success("✅ 傳承風險盤點完成")

    if st.session_state.risk_flags:
        st.markdown("### ⚠️ 您的潛在風險如下：")
        for r in st.session_state.risk_flags:
            st.markdown(f"- ❗ {r}")

        st.markdown("---")
        st.markdown("### 🎯 建議行動")
        st.markdown("每一個風險背後，都藏著一次為家族更周全準備的機會。")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 使用 AI 傳承教練"):
                st.switch_page("pages/1_coach.py")
        with col2:
            st.markdown("[📞 預約顧問諮詢](mailto:123@gracefo.com)", unsafe_allow_html=True)


    else:
        st.balloons()
        st.markdown("🎉 恭喜您，目前家族傳承結構相對完整！")

    if st.button("🔁 重新填寫"):
        st.session_state.risk_quiz_done = False
