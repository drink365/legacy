import streamlit as st

# --- 頁面設定 ---
st.set_page_config(page_title="傳承風險盤點測驗", layout="centered")

# --- 初始化狀態變數 ---
if "risk_quiz_done" not in st.session_state:
    st.session_state.risk_quiz_done = False
if "risk_flags" not in st.session_state:
    st.session_state.risk_flags = []
if "navigate" not in st.session_state:
    st.session_state.navigate = None
if "consult" not in st.session_state:
    st.session_state.consult = False

# --- 標題區 ---
st.markdown("<h1 style='text-align: center;'>🛡️ 傳承風險盤點測驗</h1>", unsafe_allow_html=True)
if not st.session_state.risk_quiz_done:
    st.markdown("請依實際情況回答以下問題，我們將快速協助您辨識家族傳承中的潛在風險。")

# --- 題目與回答輸入 ---
questions = [
    ("您的父母或長輩是否已立下遺囑？", "未立遺囑或缺乏溝通 → 財產分配易引發爭產風險"),
    ("您是否清楚目前家庭資產結構（包含股權、保單、不動產等）？", "資產結構不明 → 傳承規劃難以落實"),
    ("是否有為配偶設計足夠的保障或財產分配安排？", "配偶保障不足 → 老後可能陷入經濟風險"),
    ("您是否已開始規劃稅務影響（如贈與稅、遺產稅）？", "未提前規劃稅務 → 可能產生高額稅負"),
    ("公司股權是否有清楚的接班與移轉安排？", "公司股權未安排 → 恐影響企業穩定與家族關係"),
    ("家庭成員之間是否已共識財產分配方向？", "缺乏共識 → 潛藏親情裂痕與衝突風險")
]

# --- 風險清單產出回呼 ---
def produce_risk_list():
    flags = []
    for i, (_, risk) in enumerate(questions):
        if st.session_state.get(f"q_{i}") == "否":
            flags.append(risk)
    st.session_state.risk_flags = flags
    st.session_state.risk_quiz_done = True

# --- 互動區 ---
if not st.session_state.risk_quiz_done:
    # 收集回應並檢查
    all_answered = True
    for idx, (q, _) in enumerate(questions):
        st.radio(f"{idx+1}. {q}", ["是", "否"], key=f"q_{idx}", horizontal=True)
        if f"q_{idx}" not in st.session_state:
            all_answered = False
    # 顯示按鈕或提示
    if all_answered:
        st.button("🔍 產出我的風險清單", on_click=produce_risk_list, use_container_width=True)
    else:
        st.info("請完成所有題目後再產出風險清單。")

# --- 結果階段 ---
else:
    st.success("✅ 傳承風險盤點完成")
    if st.session_state.risk_flags:
        st.markdown("### ⚠️ 您的潛在風險如下：")
        for r in st.session_state.risk_flags:
            st.markdown(f"- ❗ {r}")
        st.markdown("---")
        st.markdown("### 🎯 建議行動")
        st.markdown("每一個風險背後，都藏著一次為家族更周全準備的機會。")
        # AI 傳承教練
        def go_to_coach():
            st.session_state.navigate = "pages/1_coach.py"
        st.button("📊 探索傳承風格", on_click=go_to_coach, use_container_width=True)
        # 預約顧問
        def make_consult():
            st.session_state.consult = True
        st.button("📞 預約顧問諮詢", on_click=make_consult, use_container_width=True)
        if st.session_state.consult:
            st.markdown("請來信至：123@gracefo.com")
    else:
        st.balloons()
        st.markdown("🎉 恭喜您，目前家族傳承結構相對完整！")
    # 重新填寫
    def reset_quiz():
        st.session_state.risk_quiz_done = False
        st.session_state.risk_flags = []
        for idx in range(len(questions)):
            st.session_state.pop(f"q_{idx}", None)
        st.session_state.consult = False
        st.session_state.navigate = None
    st.button("🔁 重新填寫", on_click=reset_quiz, use_container_width=True)

# --- 導向頁面 ---
if st.session_state.navigate:
    st.switch_page(st.session_state.navigate)

# --- 聯絡資訊 ---
st.markdown("---")
st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
      <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
      <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
      <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
